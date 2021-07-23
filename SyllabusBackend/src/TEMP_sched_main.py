from dates import Dates
from religion import ReligiousObservances
from typing import Dict, List, Tuple
from json import dump

# DELETE ME LATER
from os.path import dirname, join
from os import pardir

def merge_dicts(dates: Dict[str, str], rel: Dict[str, str]) -> Dict[str, str]:
    merged: Dict[str, str] = {}

    for key, value in dates.items():
        merged[key] = {"registrar": value, "religion": ""}

    for _rel in rel.keys():
        for date in dates.keys():
            if _rel in date:
                merged[date]["religion"] = rel[_rel]

    return merged

if __name__ == "__main__":
    MEETING_DAYS: List[int] = [0, 2, 4]
    ex_json = {
        "courseName": "DEPT XXX",
        "instructorName": "Instructor Name",
        "semester": "Fall 2021",
        "meetings": MEETING_DAYS,
        "filename": "docx/schedule for my class.docx",
        "numCols": 3,
        "landscape": 1,
        "content": {
            "Date": [],
            #"Content": [],
            #"Due": [],
            "Registrar Info": [],
            "Common Religious Observances": []
        }
    }

    aux: Dates = Dates("Fall 2021", MEETING_DAYS, 21, 22)
    #rel: ReligiousObservances = ReligiousObservances()

    #for key, value in merge_dicts(aux.get_meetings(), rel.get_observances()).items():
    for key, value in aux.get_meetings().items():
        ex_json["content"]["Date"].append(key)
        #ex_json["content"]["Content"].append("")
        #ex_json["content"]["Due"].append("")
        ex_json["content"]["Registrar Info"].append(value["registrar"])
        ex_json["content"]["Common Religious Observances"].append(value["religion"])

    with open(join(dirname(__file__), pardir, "json/ex.json"), 'w') as file:
        dump(ex_json, file, indent=4)
