from .colors import Color
from json import load
from os.path import dirname, join
from os import pardir
from .dates import Dates
from .scheduler import MeetingSchedule
from .syllabus import DOCXWriter
from sys import argv
from typing import List, Tuple

LOREM_IPSUM: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
PLACEHOLDER_TEXT: str = "Generable"


def get_academic_year(semester: str) -> Tuple[int, int]:
    curr_year = int(semester.split()[1][2:])

    if semester.split()[0] == "Fall":
        return (curr_year, curr_year + 1)

    return (curr_year - 1, curr_year)

def run_schedule():
    json_filepath = join(dirname(__file__), pardir, "../json_out/frontendoutputex.json")
    desired_filepath = join(dirname(__file__), pardir, "docx/generic_syllabus.docx")
    dict_from_json = None
    with open(json_filepath) as file:
        dict_from_json = load(file)

    year: Tuple[int, int] = get_academic_year(dict_from_json["semester"])
    dates: Dates = Dates(dict_from_json["semester"], dict_from_json["meetings"], year[0], year[1])

    schedule: MeetingSchedule = MeetingSchedule()
    schedule.build(json_filepath, return_schedule=False)



"""
def get_academic_year(semester: str) -> Tuple[int, int]:
    curr_year = int(semester.split()[1][2:])

    if semester.split()[0] == "Fall":
        return (curr_year, curr_year + 1)

    return (curr_year - 1, curr_year)


if __name__ == "__main__":
    if len(argv) == 2:
        json_filepath = join(dirname(__file__), pardir, "json/ex.json")
        desired_filepath = join(dirname(__file__), pardir, "docx/generic_syllabus.docx")

        dict_from_json = None
        with open(json_filepath) as file:
            dict_from_json = load(file)

        year: Tuple[int, int] = get_academic_year(dict_from_json["semester"])

        if argv[1].lower() == "syllabus":
            dates: Dates = Dates(dict_from_json["semester"], dict_from_json["meetings"], year[0], year[1])
            doc: DOCXWriter = DOCXWriter(dates)
            doc.populate_title("DEPT XXX - %s" % PLACEHOLDER_TEXT)
            doc.populate_course_info(name=PLACEHOLDER_TEXT, email=PLACEHOLDER_TEXT, oh_info=PLACEHOLDER_TEXT)
            doc.populate_assistant_info(name="Can choose title (TA/TF)", email=PLACEHOLDER_TEXT, oh_info=PLACEHOLDER_TEXT, tf=False)
            doc.populate_assistant_info(sname="Can choose title (TA/TF)", email=PLACEHOLDER_TEXT, oh_info=PLACEHOLDER_TEXT)
            doc.populate_generic_field("Course Overview", LOREM_IPSUM)
            doc.populate_generic_field("Course Materials", LOREM_IPSUM)
            doc.populate_grade_dist(fields={"Projects": 50, "Homework": 25, "Midterm": 10, "Final": 15}, raw_vals=False)
            doc.populate_grade_scale(max_points=1000)
            doc.populate_generic_field("Academic Dishonesty Policy", LOREM_IPSUM)
            doc.populate_generic_field("Late Policy", LOREM_IPSUM)
            doc.populate_generic_field("Attendance Policy", LOREM_IPSUM)
            doc.write(desired_filepath, json_filename=json_filepath, separate_doc=True)

        elif argv[1].lower() == "schedule":
            schedule: MeetingSchedule = MeetingSchedule()
            schedule.build(json_filepath, return_schedule=False)

        else:
            print(f"{Color.FAIL}Invalid argument, supply either 'syllabus' or 'schedule'.{Color.ENDC}")
    else:
        print(f"{Color.FAIL}Supply an arg ('syllabus', 'schedule').{Color.ENDC}")
"""