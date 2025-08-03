import os
import copy

from timetable_txt_parser import get_courses_organised
from storage_classes import CoursesAndSchedules, Section, EnrichedException
from time_management import is_compatible, convert_to_tuple_24_hours, are_identical_schedules
from export_stuff import create_new_txts, create_new_csv, save_schedule_figs

import numpy as np

def get_courses():

    timetable_dir = os.getcwd()+os.sep+"timetables"+os.sep
    timetable_files = os.listdir(timetable_dir)
    timetable_files = np.array([file for file in timetable_files if file != ".gitkeep"], dtype=object)

    timetable_paths = np.array((timetable_dir,)*timetable_files.shape[0], dtype=object)
    timetable_paths += timetable_files

    courses = get_courses_organised(timetable_dir, timetable_paths)
    assert len(courses) == len(timetable_files)

    return courses


def is_invalid_schedule(schedule : dict):
    for day, times in schedule.items():
        if len(list(set(times))) != len(times):
            return True # schedule contains duplicate times
                        # thus invalid
        for i, t1 in enumerate(times):
            for j, t2 in enumerate(times):
                if i != j:
                    if not is_compatible(t1, t2):
                        return True
    return False
        


def filter_against_mandatory_sections(mandatory_sections : CoursesAndSchedules,
                                      course : CoursesAndSchedules,
                                      defaults) -> CoursesAndSchedules:
    
    allow_intensives, complementary_language = defaults[2], defaults[3]

    allowed_sections = []

    #i = 0

    for section in course.sections:

        if section.class_type != "Intensive":
            if course.title == "complementaries":

                if complementary_language == "fr":
                    if not section.comment:
                        continue
                    elif not "french".upper() in section.comment.upper():
                        continue
                elif complementary_language == "en":
                    if section.comment:
                        if "french".upper() in section.comment.upper():
                            continue
                else:
                    raise Exception(f'language {complementary_language} not en or fr')

            elif section.comment:
                #print(section.comment)
                if any([c in section.comment for c in ["Reflections", "New School"]]):
                    continue


            section.update_schedule_dict()
            curr_schedule = copy.deepcopy(mandatory_sections.schedule_dict)

            for day, times in section.schedule_dict.items():
                curr_schedule[day].extend(times)

            if not is_invalid_schedule(curr_schedule):
                allowed_sections.append(section)
        else:
            if allow_intensives:
                allowed_sections.append(section)
            else: # don't allow intensives
                pass

    allowed = CoursesAndSchedules()
    allowed.title = course.title
    allowed.sections = allowed_sections

    return allowed


def get_mandatory_sections(courses : list[CoursesAndSchedules], defaults) -> CoursesAndSchedules:

    sections_to_include = []


    for course in courses:
        enr_sections = []
        if course.title in defaults[0]:
            for section in course.sections:
                if section.comment:
                    if "enriched".upper() in section.comment.upper():
                        enr_sections.append(section)

            if len(enr_sections)==1:
                sections_to_include.extend(enr_sections)
            elif len(enr_sections)==0:
                raise Exception(f"no enriched sections in course {course.title}")
            else:
                combos = []
                for s_i in enr_sections:
                    for s_j in enr_sections:
                        combos.append(are_identical_schedules(s_i.schedule_dict, s_j.schedule_dict))
                if all(combos):
                    sections_to_include.append(enr_sections[0])
                else:
                    raise Exception(f"{len(enr_sections)} non-identical enriched sections in course {course.title}")




    mandatory_sections = CoursesAndSchedules()

    enriched_blocks = Section()
    enriched_blocks.schedule_dict["Wednesday"].append((1300, 1430))
    enriched_blocks.schedule_dict["Friday"].append((1300, 1430))
    enriched_blocks.schedule_dict["Friday"].append((1430, 1730))
    enriched_blocks.course_title = "Enriched Science"
    enriched_blocks.graph_colour = "chocolate"
    sections_to_include.extend([enriched_blocks])

    mandatory_sections.sections = sections_to_include

    return mandatory_sections


def filter_courses_for_allowed_sections(mandatory_sections, courses, defaults) -> list[CoursesAndSchedules]:

    mandatory_sections.update_schedule_dict()
    lst_allowed = []

    for course in courses:
        if course.title in defaults[1]:
            lst_allowed.append(filter_against_mandatory_sections(mandatory_sections, course, defaults))

    return lst_allowed

def export_allowed_courses(courses):
    create_new_txts(courses)
    create_new_csv(courses)