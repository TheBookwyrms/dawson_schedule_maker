class EnrichedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Section:
    def __init__(self):
        self.course_title = None

        self.complementary_ensemble = None
        self.section_title = None
        self.section_number = None
        self.teacher = None
        self.description = None
        self.comment = None

        self.class_type = None
        self.intensive_dates = {}
        self.schedule_dict = {
            "Monday" : [],
            "Tuesday" : [],
            "Wednesday" : [],
            "Thursday" : [],
            "Friday" : [],
        }
        self.classrooms = []

        self.course_withdrawal_date = None
        self.course_drop_date = None

        self.graph_colour = None


    def update_schedule_dict(self):

        for day, timespans in self.schedule_dict.items():
            self.schedule_dict[day] = list(set(timespans))


class CoursesAndSchedules:
    def __init__(self, title=None, sections=()):
        if type(sections)==tuple:
            sections = []
        self.title = title
        self.sections : list[Section] = sections
        self.reset_schedule_dict()

    def reset_schedule_dict(self):
        self.schedule_dict = {
            "Monday" : [],
            "Tuesday" : [],
            "Wednesday" : [],
            "Thursday" : [],
            "Friday" : [],
        }

    def update_schedule_dict(self):
        self.reset_schedule_dict()
        # for a schedule
        for section in self.sections:
            for day, timespan in section.schedule_dict.items():
                #print(day, timespan)
                self.schedule_dict[day].extend(timespan)
        
        for day, timespans in self.schedule_dict.items():
            self.schedule_dict[day] = list(set(timespans))

    def __len__(self):
        return len(self.sections)
    
    def __iter__(self):
        return iter(self.sections)

    def __getitem__(self, indices):

        indexed_stuff = CoursesAndSchedules()

        if type(indices) == int:
            indexed_stuff.sections.append(self.sections[indices])
        elif type(indices) == tuple:
            for idx in indices:
                indexed_stuff.sections.append(self.sections[idx])
        elif type(indices) == slice:
            for idx in range(indices.start, indices.stop, indices.step if indices.step else 1):
                indexed_stuff.sections.append(self.sections[idx])
        else:
            raise TypeError()

        return indexed_stuff