import pandas as pd
from datetime import datetime
import random

class Scheduler():
    def __init__(self):
        pass

    def import_data(self):
        data = pd.read_csv("data/Authoritative Staff Roster, CS50 Fall 2023 - Staff List.csv")
        self.heads = data[data["staff_position"] == "Head Teaching Fellow (TF)"]
        self.tfs = data[data["staff_position"] == "Teaching Fellow (TF)"]
        self.cas = data[data["staff_position"] == "Course Assistant (CA)"]

    def set_dates(self):
        self.dates = pd.date_range(start="2023-09-05",end="2023-12-10")#.to_pydatetime().tolist()

        dates_to_remove = [(9, 7)]

        # TODO: Fix removal of dates from configuration
        remove_objects = []
        for date in self.dates:
            for month, day in dates_to_remove:
                if date.month==month and date.day == day:
                    # Fires, remove_objects contains an object
                    remove_objects.append(date)
        
        # Not removing dates as desired
        self.dates.drop(remove_objects)
        print(self.dates)

    def set_output(self):
        # Configure the number of Assignees required for each category
        self.config = {
            "Staff Member": 3,
            "Alternate Staff Member": 2
        }

        self.assignment = {}
        for date in self.dates:
            self.assignment[date] = {
                group: [None for _ in range(requirements)]
                for group, requirements in self.config.items()
            }
            self.assignment[date]["all_staff"] = set()


    def assign(self):
        """
            Handles the main assignment logic.
        """

        # Get the number of positions that need to be filled
        num_assignments = len(self.dates) * sum(self.config.values())
        to_assign = []
        assigned = 0
        for person in self.choose_next():
            if assigned >= num_assignments:
                break
            to_assign.append(person)
            assigned += 1
        
        random.shuffle(to_assign)

        # Tackle one group at a time
        for group in self.config.keys():
            for day in self.assignment.values():
                day_assignment = day[group]
                for i in range(len(day_assignment)):
                    # for _ in range(len(ineligible)):
                    #     person = ineligible.pop(0)
                    #     if person in day["all_staff"]:
                    #         ineligible.append(person)
                    #         continue
                    #     day_assignment[i] = person

                    # If we can assign the last person, do it!
                    person = to_assign.pop()
                    ineligible = []
                    while to_assign and person in day["all_staff"]:
                        ineligible.append(person)
                        person = to_assign.pop()
                    
                    day_assignment[i] = person
                    day["all_staff"].add(person)
                    to_assign = to_assign + ineligible
                        
        for day in self.assignment.items():
            print(day)

    def check_hermione(self):
        self.hermione_days = []
        for date, day in self.assignment.items():
            if len(day["all_staff"]) != 5:
                print("Hermione detected!")
                print(day)
                self.hermione_days.append(date)
        


    def switch(self, day, person_idx, role):
        
        print("Attempting switch")


        person = day[role][person_idx]
        for date, other_day in self.assignment.items():
            if day == other_day:
                continue
            if person in other_day[role]:
                continue
            for i in range(len(other_day[role])):
                other_person = other_day[role][i]
                if other_person not in day["all_staff"]:
                    day["all_staff"].add(other_person)
                    
                    # TODO: Fix that this assumes that the other person is not a Hermione too.
                    other_day["all_staff"].remove(other_person)


                    other_day["all_staff"].add(person)

                    day[role][person_idx], other_day[role][i] = other_person, person
                    print("Hermione resolved!")
                    print(day)
                    print(other_day)
                    return

                    

    def resolve_hermione(self):
        """
            Resolve Hermione conflicts requiring two locations at once
        """
        if not self.hermione_days:
            return
        
        print("Attempting Hermione fix")

        # Hermione could appear a couple of times. There could be two separate Hermiones on the same day!
        # We must tread with caution.
        for herm_day in self.hermione_days:
            seen = []
            day = self.assignment[herm_day]
            for person_idx in range(len(day["Staff Member"])):
                person = day["Staff Member"][person_idx]
                if person in seen:
                    self.switch(day, person_idx, "Staff Member")
                    seen.append(day["Staff Member"][person_idx])
                else:
                    seen.append(person)
            for person_idx in range(len(day["Alternate Staff Member"])):
                person = day["Alternate Staff Member"][person_idx]
                if person in seen:
                    self.switch(day, person_idx, "Alternate Staff Member")
                else:
                    seen.append(person)


    def choose_next(self):
        draw_group = list(self.cas.copy(deep=True)["full_preferred_name"])
        random.shuffle(draw_group)
        for person in draw_group:
            yield person
        draw_group = list(self.tfs.copy(deep=True)["full_preferred_name"])
        random.shuffle(draw_group)
        for person in draw_group:
            yield person
        draw_group = list(self.heads.copy(deep=True)["full_preferred_name"])
        random.shuffle(draw_group)
        for person in draw_group:
            yield person
        yield from self.choose_next()
        

    def write_out(self):
        data = pd.DataFrame(self.assignment).T
        # List of column names containing lists
        list_columns = self.config.keys()
        self.expand_lists_to_columns(data, list_columns)
        data.to_csv("data/out.csv")

    def expand_lists_to_columns(self, df, column_names):
        for col_name in column_names:
            max_len = df[col_name].apply(len).max()
            for i in range(max_len):
                df[f"{col_name} {i+1}"] = df[col_name].apply(lambda x: x[i] if len(x) > i else None)
            df.drop(columns=[col_name], inplace=True)
        df.drop(columns=["all_staff"], inplace=True)

    

    def test(self):
        self.import_data()
        self.set_dates()
        self.set_output()
        self.assign()
        self.check_hermione()
        self.resolve_hermione()
        # self.write_out()

sched = Scheduler()
sched.test()