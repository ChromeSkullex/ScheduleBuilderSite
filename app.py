#from app import app
from flask import Flask, send_file, render_template, request, redirect, jsonify
from SyllabusBackend.src.main import run_schedule
import json
from os.path import dirname, join
from os import pardir
from SyllabusBackend.src.dates import Dates
from typing import List, Tuple

app = Flask(__name__)

@app.route('/')
def upload_form():
	return render_template('SyllabusScheduleMaker.html')

@app.route('/', methods=['GET','POST'])
def form_data():
    if request.method == "POST":
        validate_check = request.form.getlist('meetings')
        if not validate_check:
            return ('', 204)
        file_name = createJSON()
        run_schedule()

        return send_file(file_name, as_attachment = True, cache_timeout=0)

    return ('', 204)

@app.route('/process', methods=['POST'])
def process():
    meetings_list = request.form.getlist('meetings')

    if not meetings_list:
        return jsonify({'error': 'Missing Meeting. Please Check at least one day'})


"""
NAME: createJSON()
PARAMS: NONE
DESC: Gets the form data and converts it to a JSON
RETURN: Returns the name of the json
"""
def createJSON():
    # First is convertion (Combine Semester and covert to numbers)
    # This is disgusting
    print("WHERE ARE YOU BRUH")
    req = request.form.to_dict()
    req_meetings = request.form.getlist('meetings')
    if not req_meetings:
        req["meetings"]  = [0]
    else:
        temp_list = []
        for day in req_meetings:
            temp_list.append(int(day))
        req["meetings"] = temp_list

    json_file_path ="./json_out/frontendoutputex.json"
    req["numCols"] = int(req["numCols"]) + 3
    req["landscape"] = int(req["landscape"])
    semester = "%s %s" % (req["semester1"],req["semester2"])
    req["semester"] = semester
    req.pop("semester1")
    req.pop("semester2")
    req.update({"filename": "%s_%s.docx" % (req["instructorName"], req["courseName"])})
    req.update(content_pop(semester, req["meetings"] ))
    list_empty_days = []
    for i in range(len(req['content']['Date'])):
        list_empty_days.append("")
    print(req['numCols'])
    for i in range(req['numCols'] - 3):
        temp_col = {"Blank_Col_" + str(i): list_empty_days}
        req["content"].update(temp_col)

    with open(json_file_path, 'w') as jsonfile:
        json.dump(req, jsonfile, indent=4)

    jsonfile.close()
    return req["filename"]

def get_academic_year(semester: str) -> Tuple[int, int]:
    curr_year = int(semester.split()[1][2:])

    if semester.split()[0] == "Fall":
        return (curr_year, curr_year + 1)

    return (curr_year - 1, curr_year)

"""
NAME: createJSON()
PARAMS: semester, meeting, both from createJSON(), Semester = str "Fall 2021", Meeting = list of days
DESC: Creates the content information in the json
RETURN: dict
"""
def content_pop(semester, meeting):
    # Hard coding, never heard of her
    year: Tuple[int, int] = get_academic_year(semester)
    dates: Dates = Dates(semester, meeting, year[0], year[1])
    date_dict = dates.get_meetings()
    content_dict = {"content": {"Date": [], "Registrar Info":[], "Common Religious Observances":[]}}
    date_list = []
    reg_list = []
    rel_list = []
    print(date_dict)

    for key, value in date_dict.items():
        date_list.append(key)
        reg_list.append(value["registrar"])
        rel_list.append(value["religion"])

    content_dict["content"]["Date"] = date_list
    content_dict["content"]["Registrar Info"] = reg_list
    content_dict["content"]["Common Religious Observances"] = rel_list
    return content_dict


if __name__ == "__main__":
    app.run(port=33507, debug=True)