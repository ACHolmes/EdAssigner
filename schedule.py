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

        self.assignment = {
            date: [[None for _ in range(requirements)] for requirements in self.config.values()] for date in self.dates
        }
    
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
        for group_index in range(len(self.config)):
            for day in self.assignment.values():
                day_assignment = day[group_index]
                for i in range(len(day_assignment)):
                    # If we can assign the last person, do it!
                    day_assignment[i] = to_assign.pop()
        
        print(self.assignment)
    
    def resolve_hermione(self):
        """
            Resolve Hermione conflicts requiring two locations at once
        """
                    


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
        

    def test(self):
        self.import_data()
        self.set_dates()
        self.set_output()
        self.assign()

sched = Scheduler()
sched.test()