how to use:
1) go to timetable and registration guide
2) for each course you will take next semester (excluding a complementary, if you have one):
   - search that course in the guide
   - open all windows (open all button)
   - copy entire page (ctrl-a, ctrl-c)
   - paste the page into a txt file inside of the ```timetables``` directory
     - note that some precopied ones are already there, but are likely outdated or may refer to courses of differing levels for gen eds, and should be be updated if time permits
3) for complementaries, should you have them
   - repeat the previous steps with the following modification:
   - instead of searching for all complementary courses, set a search for complementaries of the domains available to you
4) inside of ```use_schedule_maker.py```, place the name of each txt file into the respective list for it
   - as in, titles for science txt files into mandatory_courses list, titles for gen ed txt files into gen_eds list
5) set settings below the lists for whether to allow intensive courses or not, and to the language of complementary courses you would be taking
   - note for people going to DESY, it is unlikely we would be able do gym intensives, as we would miss a large portion of classes
6) run ```use_schedule_maker.py``` to print the number of possible and unique schedules you have, given the listed courses
7) optional export features include:
   - ```export_allowed_courses``` : exports txt files of the sections for all gen eds that are compatible with assigned courses for enriched science, as well as a csv with similar information collated into ```compatible_sections``` directory
   - ```export_mandatory_sections``` : exports a single image of the minimal schedule which is built by your assigned science courses into ```mandatory_stuff``` directory
   - ```export_images``` : exports images of all unique schedules without and with including gym variants into the ```unique_schedules_no_gym``` and ```unique_schedules_with_gym``` directories, respectively