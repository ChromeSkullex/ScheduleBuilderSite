"""
    Working on this through webstorm so syntax may be incorrent
    Converting load Data from .py to .js using AJAX and jquery
    Get all the dates for the semester, name json fall_2021.json by semester and year
    Fell free to refactor this, this is merely a draft to get ideas down, at least to get it working

    json:
    {
        'semester': "Fall 2021"
        'num': 76,
        'context':
            'Dates':
                []
            'empty':
                [true, false]

    }


"""

from parsepdf import ParseDates
import json # will change to from import
from os import pardir
from os.path import dirname, join

if __name__ == '__main__':
    print("Works")
    dates = ParseDates("Fall 2021", [0, 2, 4], 21, 22)
    json_filepath = join(dirname(__file__), pardir, "json/fall_2021.json")
    list_dates = dates.get_meetings()
    date_dict = {"semester": "Fall 2021", "num": len(list_dates), "context": {"Dates": [], "Empty": [], "Content":[]}}  # Most likely temp, but its here

    # need to convert this data to JSON
    # print(dates)
    """
    print(date_dict["context"]["Dates"])
    date_dict["context"]["Dates"] = list_dates
    print(date_dict["context"]["Dates"])"""

    # Gonna check if there is holiday/extra content, also checks if its empty (to make it easier for converting js)
    for i in range(len(list_dates)):
        print(0,list_dates[0].split())
        # More than just the dates, we empty == false and content is added
        check_date = list_dates[i].split()
        if (len(check_date) > 3):
            renew_date = ""
            for spl_num in range(0, 3):
                renew_date += check_date[spl_num] + " "
            date_content = ""
            for j in range(4,len(check_date)):
                date_content += check_date[j] + " "
            print(date_content)
            date_dict["context"]["Dates"].append(renew_date)
            date_dict["context"]["Empty"].append(False)
            date_dict["context"]["Content"].append(date_content)
        else:
            date_dict["context"]["Dates"].append(list_dates[i])
            date_dict["context"]["Empty"].append(True)
            date_dict["context"]["Content"].append(" ")
    print( date_dict["context"]["Empty"])

    with open(json_filepath, 'w') as file:
        json.dump(date_dict, file, indent=4)