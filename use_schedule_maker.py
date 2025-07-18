from schedule_possibilities import (get_all_allowed_gen_eds, iterate_for_possible_schedules,
                                    get_unique_schedules, export_allowed_courses,
                                    export_mandatory_sections, export_schedules)


allow_intensive_courses = False
complementary_language = "fr"
complementary_filename = "complementaries"


mandatory_courses = [
    "Algébre Linéaire et Géométrie Vectorielle",
    "Engineering Physics",
    "Probability and Statistics",
    "Waves and Modern Physics",
]
gen_eds = [
    "Applied Ethics in Humanities",
    "Literary Themes",
    "Physical Activity and Health",
    complementary_filename,
]


defaults = (mandatory_courses, gen_eds, allow_intensive_courses, complementary_language)




allowed_sections, mandatory_sections = get_all_allowed_gen_eds(defaults)

possible_sch_no_gym = iterate_for_possible_schedules(mandatory_sections, allowed_sections[:-1], origin=True)
possible_sch_with_gym = iterate_for_possible_schedules(mandatory_sections, allowed_sections, origin=True)

unique_sch_no_gym = get_unique_schedules(possible_sch_no_gym)
unique_sch_with_gym = get_unique_schedules(possible_sch_with_gym)

#export_allowed_courses(allowed_sections)
#export_mandatory_sections([mandatory_sections])
#export_schedules(unique_sch_no_gym, unique_sch_with_gym)

#print(mandatory_sections.schedule_dict)

for course in allowed_sections:
    print(len(course), "compatible courses in", course.title)


#print()
#print('''IMPORTANT NOTE: unique timeslots means
#                schedules whose timeslots result in equivalent
#                schedules, regardless of the courses
#                or sections that make them up''')
print()
print(f'{len(possible_sch_no_gym)} possible schedules, before iterating through gyms')
print(f'{len(possible_sch_with_gym)} possible schedules, iterating through gyms')
print(f'{len(unique_sch_no_gym)} schedules with unique timeslots, before iterating through gyms')
print(f'{len(unique_sch_with_gym)} schedules with unique timeslots, iterating through gyms')
