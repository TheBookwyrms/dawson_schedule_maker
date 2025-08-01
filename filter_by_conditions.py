def filter_by_conditions(possible_schedules):
    filtered_sch = []
    for schedule in possible_schedules:
        for section in schedule.sections:
            if section.course_title == "Applied Ethics in Humanities":
                if section.section_title == "Science Fiction and Ethics":
                    filtered_sch.append(schedule)
    return filtered_sch