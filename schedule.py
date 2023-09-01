import pandas as pd
import random


class Scheduler():
    def configure(self):
        """
            Handles the configuration of the script. This is the only place you should need to edit
            each semester to generate a new Ed assignment.
        """

        # Set the path to the authoritative staff roster CSV file. Export this from the Google Sheet!
        self.staff_roster_file = "data/Authoritative Staff Roster, CS50 Fall 2023 - Staff List.csv"
        
        # Configure the number of Assignees required for each category. Normally
        # we have 3 staff and 2 backups.
        self.config = {
            "Staff Member": 3
            # "Alternate Staff Member": 2 -> we used to have assigned 'backup staff'
            # another example could be a head TF 'monitor' or something
            # Currently we just use it to have 3 staff members
        }

        # Configure the dates for which we need staff assignments.
        # Easiest to create a range for the whole semester and then remove some.
        dates = pd.date_range(start="2023-09-05",end="2023-12-10")

        # Dates we don't need to assign, format: (MM, DD)
        dates_to_remove = set([(11, 22), (11, 23), (11, 24), (11, 25), (11, 26)])

        remove_objects = []
        
        # Iterate through all dates and remove
        for date in dates:
            if (date.month, date.day) in dates_to_remove:
                # Fires, remove_objects contains an object
                remove_objects.append(date)
        
        # Remove unwanted days
        self.dates = dates.drop(remove_objects)

        self.out_file_path = "data/generated_assignment.csv"

        # Now all configured and good to go! We have the staff info, dates and roles required :)


    def import_data(self):
        """ Reads in the data from the Staff list CSV file. """
        data = pd.read_csv(self.staff_roster_file)
        self.heads = data[data["staff_position"] == "Head Teaching Fellow (TF)"]["full_preferred_name"].tolist()
        self.tfs = data[data["staff_position"] == "Teaching Fellow (TF)"]["full_preferred_name"].tolist()
        self.cas = data[data["staff_position"] == "Course Assistant (CA)"]["full_preferred_name"].tolist()

    def add_staff(self):
        """Manually inserts staff into the system. Can be just 'pass' if not needed."""

        self.tfs += [
            "Alec Whiting",
            "Christo Savalas",
            "Daniel Chang",
            "Guy White",
            "Margaret Tanzosh",
            "Taha Teke"
        ]
            

        self.cas += [
            "Bradley Ross"
        ]

    def set_output(self):
        """
            Configures the output requiremenets. What Staff categories do we have in terms of Ed, and how many are needed for each, each day?
            Also initializes the self.assignment attribute to store the output assignment.
        """
        # Initialize empty assignment
        self.assignment = {}
        for date in self.dates:

            # Initially nobody assigned to any role
            self.assignment[date] = {
                group: [None for _ in range(requirements)]
                for group, requirements in self.config.items()
            }

            # And all_staff is an empty set for each day
            self.assignment[date]["all_staff"] = set()


    def assign(self):
        """
            Handles the main assignment logic.
        """

        # Get the number of positions that need to be filled, and initialize to_assign list to keep track of who we need to assign.
        num_assignments = len(self.dates) * sum(self.config.values())
        to_assign = []
        assigned = 0
        
        # Pull people from the generator that chooses the next staff member who should be assigned.
        for person in self.choose_next():
            if assigned >= num_assignments:
                break
            to_assign.append(person)
            assigned += 1
        
        # Randomly shuffle the whole list of staff we need to assign.
        random.shuffle(to_assign)

        # Tackle one role at a time
        for group in self.config.keys():

            # For each days
            for day in self.assignment.values():
                day_assignment = day[group]

                # We fill each role for the day
                for i in range(len(day_assignment)):

                    # While trying to assign, we may have inelgible people (already assigned to that day). Array to keep track of them.
                    ineligible = []

                    # Get a person that we need to assign
                    person = to_assign.pop()
                    
                    # While the current person we are considering is inelgible (they are in the day's staff already)
                    # Add them to the inelgible list, and get someone else that we need to assign
                    while to_assign and person in day["all_staff"]:
                        ineligible.append(person)
                        person = to_assign.pop()
                    
                    # Either this person is now safe to assign, or we ran out of options. We'll fix this later if we ran out of options in resolve_hermiones.
                    # For now, just assign them!
                    day_assignment[i] = person
                    day["all_staff"].add(person)

                    # Update the to_assign list to put the inelgible people back. Putting them
                    # at the front so that the next role for the day, we don't consider the same people again immediately.
                    to_assign = ineligible + to_assign

    def check_hermione(self):
        """
            Checks whether there are any days where one (or more people) are assigned more than once for the day.
            I call these Hermiones, as she would attend two classes at once with her time gadget. We can't allow that here!
        """

        # Days where Hermione shows up!
        self.hermione_days = []

        for date, day in self.assignment.items():

            # If the number of unique staff assigned to a day isn't correct, we have spotted (one or more) Hermione(s)! 
            if len(day["all_staff"]) != sum(self.config.values()):
                print("Hermione detected!")
                print(day)
                self.hermione_days.append(date)
        


    def switch(self, day, person_idx, role):
        """
            Function to switch a Hermione from one day to any other she isn't currently working on, in the same role as before.

            Args:
                day: the day assignment object wherein Hermione is up to mischief.
                person_idx: the index of the Hermione in that day and role.
                role: The role Hermione is in for which we wish to move her to another day.
        """

        # Here's Hermione, on the original day.
        person = day[role][person_idx]

        # We need to move Hermione to another day, let's just iterate through our options
        for _, other_day in self.assignment.items():

            # Don't bother with keeping her on the same day
            if day == other_day:
                continue

            # Don't move her to a different day where she's already working
            if person in other_day["all_staff"]:
                continue

            # She's not working that day then. Let's look through possible people she can switch with
            for i in range(len(other_day[role])):

                # Here's other_person, who we might want to switch with our Hermione
                other_person = other_day[role][i]

                # If they are working on the same day as Hermione, we can't switch them, else they would become Hermione too!
                if other_person in day["all_staff"]:
                    continue

                # Else we can safely switch them!
                
                # Add the other person to Hermione's day all_staff
                day["all_staff"].add(other_person)
                
                # And Hermione to their day's all_staff
                other_day["all_staff"].add(person)

                # Remove the other person from their original day's all_staff. 
                # They weren't up to no good, so switching them means they no longer work that day.
                # TODO: Fix that this assumes that the other person is not a Hermione too.
                other_day["all_staff"].remove(other_person)

                # Hermione is not removed from all_staff on her original day, as she was there more than once. Making this switch doesn't remove her from the day
                # just stops her from doing multiple things that day.

                # Make the switch
                day[role][person_idx], other_day[role][i] = other_person, person
                print("Hermione resolved!")
                print(day)
                return

                    

    def resolve_hermione(self):
        """
            Resolve Hermione conflicts requiring two locations at once. Calls self.switch to switch Hermione around
            to obey a valid schedule with no more than one task at any one time.
        """

        # If no Hermiones, no problem!
        if not self.hermione_days:
            return

        # For each day we see Hermione acting suspicious, we must correct her behaviour
        for herm_day in self.hermione_days:

            # Staff names we've seen so far today
            seen = []

            # The info for the day in question
            day = self.assignment[herm_day]

            # For each role we need to fill that day
            for role in self.config.keys():

                # For each person assigned to that role
                for person_idx in range(len(day[role])):
                    person = day[role][person_idx]

                    # If we've seen them already today, it's Hermione! We must switch around her schedule to play nice.
                    if person in seen:
                        self.switch(day, person_idx, role)
                        seen.append(day[role][person_idx])
                    
                    # Else we register the attendance of a well behaved wizard.
                    else:
                        seen.append(person)



    def choose_next(self):
        """
            Generator to give the next person who should be assigned a job.
            Draws from CAs, then TFs, then Head TFs in a loop so that CAs, then TFs most likely to get one extra day.
        """
        draw_group = self.cas.copy()
        random.shuffle(draw_group)
        for person in draw_group:
            yield person
        draw_group = self.tfs.copy()
        random.shuffle(draw_group)
        for person in draw_group:
            yield person
        draw_group = self.heads.copy()
        random.shuffle(draw_group)
        for person in draw_group:
            yield person
        yield from self.choose_next()
        

    def write_out(self):
        data = pd.DataFrame(self.assignment).T
        # List of column names containing lists
        self.expand_lists_to_columns(data)
        data.to_csv(self.out_file_path)

    def expand_lists_to_columns(self, df):
        for col_name in self.config.keys():
            max_len = df[col_name].apply(len).max()
            for i in range(max_len):
                df[f"{col_name} {i+1}"] = df[col_name].apply(lambda x: x[i] if len(x) > i else None)
            df.drop(columns=[col_name], inplace=True)
        df.drop(columns=["all_staff"], inplace=True)

    

    def pipeline(self):
        self.configure()
        self.import_data()
        self.add_staff()
        self.set_output()
        self.assign()
        self.check_hermione()
        self.resolve_hermione()
        self.write_out()

sched = Scheduler()
sched.pipeline()