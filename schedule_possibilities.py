from storage_classes import CoursesAndSchedules, Section

from timetable_analysis import get_courses, get_mandatory_sections
from timetable_analysis import filter_courses_for_allowed_sections
from export_stuff import create_new_txts, create_new_csv

from time_management import is_compatible, are_slots_compatible, are_identical_schedules, are_conflicting_schedules


def get_all_allowed_gen_eds(defaults):
    courses = get_courses()
    mandatory_sections = get_mandatory_sections(courses, defaults)
    allowed_sections = filter_courses_for_allowed_sections(mandatory_sections, courses, defaults)
    
    return allowed_sections, mandatory_sections




def section_is_already_counted(desired_section:CoursesAndSchedules|Section,
                               sections_seen:list[CoursesAndSchedules|Section]):
    
    is_seen = []

    if len(sections_seen) >= 1:
        desired_dict = desired_section.schedule_dict
        seen_dicts = [seen.schedule_dict for seen in sections_seen]

        for schedule_to_compare_with in seen_dicts:
            is_seen.append(are_identical_schedules(desired_dict,
                                                schedule_to_compare_with))
        
    return any(is_seen)


def section_is_counted(desired_section:Section,
                        sections_seen:list[Section]):
    
    is_seen = []

    if len(sections_seen) >= 1:
        desired_num = desired_section.section_number
        seen_nums = [seen.section_number for seen in sections_seen]

        for schedule_to_compare_with in seen_nums:
            is_seen.append(desired_num==schedule_to_compare_with)
            #is_seen.append(are_identical_schedules(desired_num,
            #                                    schedule_to_compare_with))
        
    return any(is_seen)


def iterate_for_possible_schedules(mandatory_sections:CoursesAndSchedules=(),
                             next_iter_items:list[Section]=(),
                             current_sections_iterated:tuple[Section]=(),
                             schedule_possibilities:tuple[CoursesAndSchedules]=(),
                             origin=False):
    
    #print(len(next_iter_items))
    #print(len(current_sections_iterated))
    #print(len(schedule_possibilities))

    timeslots_seen = []

    if next_iter_items == []:
        this_schedule = CoursesAndSchedules()
        this_schedule.sections.extend(mandatory_sections.sections)
        this_schedule.sections.extend(current_sections_iterated)
        this_schedule.update_schedule_dict()
        return schedule_possibilities+(this_schedule,)

    for section in next_iter_items[0].sections:
        #if not section_is_already_counted(section, timeslots_seen):
        #if True:
        if not section_is_counted(section, timeslots_seen):
            if any([are_conflicting_schedules(item, section) for item in current_sections_iterated]):
                continue
            else:
                timeslots_seen.append(section)
                curr_sections = current_sections_iterated+(section,)
                schedule_possibilities = iterate_for_possible_schedules(
                                                    mandatory_sections=mandatory_sections,
                                                    next_iter_items=next_iter_items[1:],
                                                    current_sections_iterated=curr_sections,
                                                    schedule_possibilities=schedule_possibilities)

    if origin:
        schedules = CoursesAndSchedules()
        schedules.sections = schedule_possibilities

        schedule_possibilities = schedules

    return schedule_possibilities


def get_unique_schedules(possible_schedules:CoursesAndSchedules):
    unique_schedules : CoursesAndSchedules = CoursesAndSchedules()

    for i, schedule in enumerate(possible_schedules):
        if not section_is_already_counted(schedule, unique_schedules):
            unique_schedules.sections.append(schedule)

    return unique_schedules



def export_allowed_courses(allowed_courses):
    create_new_txts(allowed_courses)
    create_new_csv(allowed_courses)