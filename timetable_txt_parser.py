from storage_classes import CoursesAndSchedules, Section
        
from time_management import convert_to_tuple_24_hours

import numpy as np


def get_courses_organised(dir, filepaths):

    name_preamble = len(dir)
    txt_end = -4

    courses : list[CoursesAndSchedules] = []

    colours = ["red", "blue", "green", "purple", "orange", "yellow", "deeppink", "dimgray", "darkgoldenrod", "cyan"]

    for txt, c in zip(filepaths, colours):
        
        course_name = txt[name_preamble:txt_end]

        this_course = CoursesAndSchedules()
        this_course.title = course_name

        with open(txt, "r", errors="ignore", encoding="utf-8") as file:
            page = np.array([line.lstrip() for line in file.read().split("\n") if line != ""],dtype=object)

            sections = make_course(this_course,
                                   page,
                                   c,
                                   course_name)

        this_course.sections = sections
        courses.append(this_course)

    return courses


def make_course(course:CoursesAndSchedules, page:list[str], graph_colour:str, course_name:str):
    sections = []

    first_section = True
    this_section = False
    section_made = False
    current_ensemble = None
    in_schedule = False


    for idx, line in enumerate(page):
        if "- Ensemble" in line:
            in_schedule = False
            current_ensemble = line
        elif line=="Section Title":
            if not first_section:
                this_section.graph_colour = graph_colour
                this_section.course_title = course_name
                sections.append(this_section)
            in_schedule = False
            this_section = Section()
            section_made = True
            this_section.section_title = page[idx+1]
        elif line == "Section":
            in_schedule = False
            if not section_made:
                if not first_section:
                    this_section.graph_colour = graph_colour
                    this_section.course_title = course_name
                    sections.append(this_section)
                this_section = Section()
            if current_ensemble:
                this_section.complementary_ensemble = current_ensemble
            this_section.section_number = page[idx+1]
        elif line == "Teacher":
            this_section.teacher = page[idx+1]
        elif line == "Description":
            this_section.description = page[idx+1]
        elif line == "Comment":
            comm = ""
            if page[idx+2]=="Withdrawal Date":
                comm += page[idx+1]
            else:
                comm = comm + page[idx+1] + page[idx+2]
            this_section.comment = comm
        elif line == "Withdrawal Date":
            this_section.course_withdrawal_date = page[idx+1]
        elif line == "Drop Date":
            this_section.course_drop_date = page[idx+1]
        elif line == "Schedule":
            first_section = False
            section_made = False
            in_schedule = True

        if in_schedule and line != "Schedule":
            line_items = line.split("\t")

            if len(line_items) == 4: # normal class
                weekday = line_items[0]
                unconverted_time = line_items[1]
                time = convert_to_tuple_24_hours(unconverted_time.split(" - "))
                classroom = line_items[2]
                class_type = line_items[3]

                this_section.class_type = class_type
                this_section.schedule_dict[weekday].append(time)
                this_section.classrooms.append(classroom)

            elif len(line_items) == 6: # gym intensive
                assert line_items[1] == line_items[2]
                intensive_date = line_items[1]
                unconverted_intensive_time = line_items[3]
                intensive_time = convert_to_tuple_24_hours(unconverted_intensive_time.split(" - "))
                classroom = line_items[4]
                class_type = line_items[5]

                this_section.class_type = class_type
                try:
                    this_section.intensive_dates[intensive_date].append(intensive_time)
                except:
                    this_section.intensive_dates[intensive_date] = [intensive_time]
                this_section.classrooms.append(classroom)

            if idx+1 != len(page):
                next_line = page[idx+1].split("\t")
                if len(next_line) not in [4, 6]:
                    if page[idx+1] not in ["Section Title", "Section"]:
                        current_ensemble = None

    this_section.graph_colour = graph_colour
    this_section.course_title = course_name
    sections.append(this_section)

    return sections