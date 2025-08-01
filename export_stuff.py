from storage_classes import CoursesAndSchedules, Section

from time_management import convert_to_string_12_hrs

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tqdm


def create_new_txts(courses : list[CoursesAndSchedules]):

    folder_dir = f'compatible_sections{os.sep}'

    for course in courses:
        with open(f'{folder_dir}compatible {course.title}.txt', "w+", encoding="utf-8") as txt:
            def newline():
                txt.write("\n")
            for section in course.sections:
                if section.complementary_ensemble != None:
                    txt.write(f'{section.complementary_ensemble}')
                    newline()

                txt.write(f'Section Title : {section.section_title}')
                newline()

                txt.write(f'Section : {section.section_number}')
                newline()

                txt.write(f'Teacher : {section.teacher}')
                newline()

                txt.write(f'Description : {section.description}')
                newline()

                if section.comment != None:
                    txt.write(f'Comment {section.comment}')
                    newline()

                txt.write(f'Withdrawal Date : {section.course_withdrawal_date}')
                newline()

                txt.write(f'Drop Date : {section.course_drop_date}')
                newline()

                txt.write(f"Classrooms include : {section.classrooms}")
                newline()
                if section.class_type == "Intensive":
                    txt.write("Intensive class dates : ")
                    for day, timeslot in section.intensive_dates.items():
                        newline()
                        txt.write(f"{day} : {timeslot}")
                else:

                    txt.write("Schedule :")
                    for day, timeslot in section.schedule_dict.items():
                        newline()
                        txt.write(f"{day} : {timeslot}")
                newline()
                newline()
                newline()

def create_new_csv(courses : list[CoursesAndSchedules]):
    arr = np.array([len(c.sections) for c in courses])
    x = arr.max() + 1
    y = len(courses)
    shape = (x, y)
    data = np.empty(shape, dtype=object)
    data[0, :] = [course.title for course in courses]
    for idx, course in enumerate(courses):
        for i, section in enumerate(course.sections):
            ensemble = section.complementary_ensemble
            title = section.section_title
            num = section.section_number
            teacher = section.teacher
            if section.class_type != "Intensive":
                schedule = "\n".join([f'''{day}: {
                    convert_to_string_12_hrs(timeslot)
                    }''' for day, timeslot in section.schedule_dict.items() if timeslot != []])
            else:
                schedule = "See Timetable and Registration Guide for more details"
            schedule_str = schedule
            #if len(schedule)==1:
            #    schedule_str = "\t".join(schedule[0])
            #else:
            #    k = ["\t".join(timeslot) for timeslot in schedule]
            #    print(k)
            #    schedule_str = "\n".join(k)
            info = title+"\n" if title != None else ""
            ensemble = ensemble+"\n" if ensemble != None else ""
            mandatory_info = (f"Section {num}"+"\n"
                              +f'Teacher {teacher}'+"\n"
                              +f'Schedule'+"\n"
                              +f'{schedule_str}')
            info = ensemble+info+mandatory_info
            data[i+1, idx] = info
            #print(data[0, :])
    df = pd.DataFrame(data)

    folder_dir = f'compatible_sections{os.sep}'

    df.to_csv(f"{folder_dir}compatible courses.csv")



def save_schedule_figs(unique_schedules:tuple[CoursesAndSchedules], folder_name, show_var=True):
    fdir = f'schedule_figs{os.sep}{folder_name}'
    if not os.path.exists(fdir):
        os.mkdir(fdir)
    with open(f'{fdir}{os.sep}.gitkeep', "w+") as d:
        pass

    var = 0
    schedule_idx = 0
    for idx, unique_schedule in (tqdm.tqdm(enumerate(unique_schedules),
                                          total=len(unique_schedules))):

        fig, ax = plt.subplots()

        ax.bar("Monday", height=0, bottom=1500)
        ax.bar("Tuesday", height=0, bottom=1500)
        ax.bar("Wednesday", height=0, bottom=1500)
        ax.bar("Thursday", height=0, bottom=1500)
        ax.bar("Friday", height=0, bottom=1500)



        if show_var:
            if ((unique_schedules[idx].sections[:-1] == unique_schedules[idx-1].sections[:-1])
                and (idx!=0)):
                var += 1
            else:
                var = 1
            if var==1:
                schedule_idx+= 1
        else:
            schedule_idx+= 1

        labels_added = []
        bars = []
        for idx, section in enumerate(unique_schedule.sections):           

            colour = section.graph_colour
            course = section.course_title
            if course != "Enriched Science":
                course = course[:4]
            else:
                course = "Enriched"
            number = section.section_number
            label = course+": "+number if number != None else course


            for day, value in section.schedule_dict.items():
                for time in value:
                    #print(value, len(value))
                    if len(value)!=0:
                        stuff = (day, int(time[0]), int(time[1]), colour, label)
                        #print(stuff)
                        bars.append(stuff)

        for bar in bars:
            #print("k", bar)
            if bar[-1] not in labels_added:
                ax.bar(bar[0], height=bar[2]-bar[1], bottom=bar[1], color=bar[3], label=bar[-1])
                labels_added.append(bar[-1])
            else:
                ax.bar(bar[0], height=bar[2]-bar[1], bottom=bar[1], color=bar[3])


        plt.tight_layout()
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.subplots_adjust(right=0.74)
        v = f'_var_{var}' if show_var else ""
        plt.savefig(f'{fdir}{os.sep}schedule_{schedule_idx}{v}')
        plt.close(fig)
        #plt.show()