from storage_classes import CoursesAndSchedules, Section

from datetime import datetime
import numpy as np



def is_compatible(desired_slot, slot_to_check):
    s1, e1 = desired_slot
    s2, e2 = slot_to_check

    s1, e1 = int(s1), int(e1)
    s2, e2 = int(s2), int(e2)

    assert s1 < e1
    assert s2 < e2

    if e2 <= s1: # e2 is bigger than s2. e2 is smaller than s1, thus is good
        return True
    elif s2 >= e1: # s2 is bigger than e1, thus is good
        return True

    return False


def are_slots_compatible(desired_slot, slot_to_check):
    for timeslot in desired_slot:
        for checkslot in slot_to_check:
            if not any([len(timeslot) == 6, len(checkslot) == 6]):
                if timeslot[0] == checkslot[0]:
                    if not is_compatible(timeslot[1], checkslot[1]):
                        return False
    return True
    
def convert_to_tuple_24_hours(times):
    times_lst = ["".join(
        [char for char in datetime.strftime(datetime.strptime(t, "%I:%M %p"), "%H:%M") if char.isnumeric()]
        ) for t in times]
    return tuple(times_lst)


def convert_to_string_12_hrs(times):
    times = list(times[0])
    string = " - ".join([datetime.strftime(
        datetime.strptime(
            t[:2]+":"+t[2:], "%H:%M"), "%I:%M %p") for t in times])
    
    return string



def are_identical_schedules(schedule_1, schedule_2):
    schedules : list[dict] = []


    for sch in [schedule_1, schedule_2]:
        if type(sch) == dict:
            schedules.append(sch)
        else:
            raise ValueError(f"func are_identical_schedules must receive dict, not {type(sch)}")
    assert len(schedules) == 2
    
    identical = []

    for (d0, v0), (d1, v1) in zip(schedules[0].items(), schedules[1].items()):
        if len(v0)==len(v1):
            for t in v0:
                identical.append(t in v1)
        else:
            return False
        
    if all(identical):
        return True
    else:
        return False
    

def are_conflicting_schedules(schedule_1 : CoursesAndSchedules | Section, schedule_2 : CoursesAndSchedules | Section):
    schedules : list[dict] = []

    for sch in [schedule_1, schedule_2]:
        if type(sch) == CoursesAndSchedules:
            sch.update_schedule_dict()
            schedules.append(sch.schedule_dict)
        elif type(sch) == Section:
            schedules.append(sch.schedule_dict)

    assert len(schedules) == 2

    compatible = []
    for (d0, v0), (d1, v1) in zip(schedules[0].items(), schedules[1].items()):
        for t0 in v0:
            for t1 in v1:
                if not t0==t1==[]:
                    compatible.append(is_compatible(t0, t1))

    if not all(compatible):
        return True
    else:
        return 
    
def is_possible_schedule(schedule:CoursesAndSchedules):
    for day, times in schedule.schedule_dict.items():
        for i, t1 in enumerate(times):
            for j, t2 in enumerate(times):
                if i!=j:
                    if not is_compatible(t1, t2):
                        return False
    
    #print()
    #print()
    return True