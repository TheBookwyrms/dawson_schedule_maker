from schedule_possibilities import (get_all_allowed_gen_eds, iterate_for_possible_schedules,
                                    get_unique_schedules, export_allowed_courses)
from filter_by_conditions import filter_by_conditions
from export_stuff import save_schedule_figs


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

filt_poss_no_gym = filter_by_conditions(possible_sch_no_gym)
filt_poss_with_gym = filter_by_conditions(possible_sch_with_gym)

unique_sch_no_gym = get_unique_schedules(possible_sch_no_gym)
unique_sch_with_gym = get_unique_schedules(possible_sch_with_gym)

#print(f'{unique_sch_with_gym=}'.split('=')[0])

export_allowed_courses(allowed_sections)
#save_schedule_figs([mandatory_sections], folder_name=f'{mandatory_sections=}'.split('=')[0], show_var=False)
#save_schedule_figs(filt_poss_no_gym, folder_name=f'{filt_poss_no_gym=}'.split('=')[0], show_var=False)
#save_schedule_figs(filt_poss_with_gym, folder_name=f'{filt_poss_with_gym=}'.split('=')[0], show_var=True)
#save_schedule_figs(unique_sch_no_gym, folder_name=f'{unique_sch_no_gym=}'.split('=')[0], show_var=True)
#save_schedule_figs(unique_sch_with_gym, folder_name=f'{unique_sch_with_gym=}'.split('=')[0], show_var=True)

#print(mandatory_sections.schedule_dict)

for course in allowed_sections:
    print(len(course), "compatible courses in", course.title)


print()
print(f'{len(possible_sch_no_gym)} possible schedules, before iterating through gyms')
print(f'{len(possible_sch_with_gym)} possible schedules, iterating through gyms')
print(  f'{len(filt_poss_no_gym)}, {len(filt_poss_no_gym[0])} `` ``, `` `` `` ``, only hum 03 and eng 19,   6 hopefully')
print(f'{len(filt_poss_with_gym)} `` ``, `` `` ``, only hum 03 and eng 19')
print(f'{len(unique_sch_no_gym)} schedules with unique timeslots, before iterating through gyms')
print(f'{len(unique_sch_with_gym)} schedules with unique timeslots, iterating through gyms')


for section in allowed_sections[2].sections:
    if section.section_title == "Time Travel in Literature":
        t = section.schedule_dict
    #print(section.section_number, section.section_title)

l = []
for i, schedule in enumerate(possible_sch_with_gym):
    for section in schedule.sections:
        if section.course_title == "Literary Themes":
            if section.schedule_dict == t:
                l = set(list(l)+[section.section_number])
                #print(i, section.course_title, section.section_number, section.section_title)

print(t)
print(l)

for schedule in filt_poss_no_gym[0]:
    print(schedule.schedule_dict)