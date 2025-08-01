def filter_by_conditions(possible_schedules):
    filtered_sch = []
    for schedule in possible_schedules:
        eth = False
        eng = False
        for section in schedule.sections:
            if section.course_title == "Applied Ethics in Humanities":
                if section.section_title == "Science Fiction and Ethics":
                    eth = True

        for section in schedule.sections:
            if section.course_title == "Literary Themes":
                if section.section_title == "Time Travel in Literature":
                    eng = True


        if eng:
            filtered_sch.append(schedule)
    return filtered_sch