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

        # Tackle one group at a time
        for group in self.config.keys():
            for day in self.assignment.values():
                day_assignment = day[group]
                for i in range(len(day_assignment)):
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
        for day in self.assignment.values():
            if len(day["all_staff"]) != 5:
                print("Hermione detected!")
                print(day)
                break
        else:
            print("No Hermiones detected")

    def resolve_hermione(self):
        """
            Resolve Hermione conflicts requiring two locations at once
        """
        pass


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
        self.write_out()

sched = Scheduler()
sched.test()