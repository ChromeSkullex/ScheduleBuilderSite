from calendar import Calendar
from .colors import Color
from .exceptions import RegPDFErr
from PyPDF2 import PdfReader
from requests import get as req_get, models
from typing import List, Dict, Iterator, Tuple

# for testing
from inspect import currentframe

class ParseDates:
    FIRST_DAY: str = "first day of classes"
    LAST_DAY: str = "last day of classes"
    FINAL_EXAMS: str = "final exams"

    MONTHS: List[str] = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    SEMESTER_MONTHS: Dict[str, List[int]] = {
        "Fall": [
            8, 9, 10, 11, 12
        ],
        "Winter": [
            1
        ],
        "Spring": [
            1, 2, 3, 4, 5
        ],
        "Summer": [
            6, 7, 8
        ]
    }
    WEEKDAYS: List[str] = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    def __init__(self, semester: str, meeting_days: List[int], fall_year: int, spring_year: int):
        self._calendar: Calendar = Calendar(0)
        self._semester: str = semester
        self._meeting_days: List[int] = meeting_days
        self._fall_year: int = fall_year
        self._spring_year: int = spring_year
        self._file_path: str = None
        self._flavored_dates: Dict[str, str] = {}

        self._build()

    def _build(self) -> None:
        self._file_path: str = self._download_schedule()
        self._parse_pdf()
        self._flavored_dates = self._get_meeting_dates(self._flavored_dates)

        print("%-25s %-30s %5s" % (__name__, currentframe().f_code.co_name, f"{Color.OKCYAN}Done!{Color.ENDC}"))

        return

    def _download_schedule(self) -> str:
        print("%-25s %-30s %10s" % (__name__, currentframe().f_code.co_name, "Downloading PDF..."))

        url: str = "https://registrar.umbc.edu/files/2015/04/20%d-%d.pdf" % (self._fall_year, self._spring_year)
        pdf_request: models.Response = req_get(url)

        if pdf_request.status_code != 200: raise RegPDFErr("Failed to fetch registrar PDF.")
        pdf_name: str = "f%ds%d.pdf" % (self._fall_year, self._spring_year)

        with open(pdf_name, "wb") as file:
            file.write(pdf_request.content)

        return pdf_name

    def _parse_pdf(self) -> None:
        print("%-25s %-30s %10s" % (__name__, currentframe().f_code.co_name, "Parsing PDF..."))

        # set all semester variations for this academic year
        semesters: List[str] = [
            "Fall 20%s" % self._fall_year,
            "Winter 20%s" % self._spring_year,
            "Spring 20%s" % self._spring_year,
            "Summer 20%s" % self._spring_year
        ]

        # remove the one semester we actually will be getting the info for
        semesters.remove(self._semester)

        # retrieve the text from the calendar PDF
        content = None
        with open(self._file_path, "rb") as file:
            pdf: PdfReader = PdfReader(file)
            content: str = pdf.pages[0].extract_text()

        content_split: List[str] = content.split('\n')

        # cut any semester information we don't need prior to finding the semester
        # we're targeting
        for i in range(len(content_split)):
            if self._semester in content_split[i]:
                content_split = content_split[i:]
                break

        # same as above, but for everything after
        chopped: bool = False
        for i in range(len(content_split)):
            for sem in semesters:
                if sem in content_split[i]:
                    content_split = content_split[:i]
                    chopped = True
                    break

            if chopped: break

        # cut the semester out from the data (i.e. remove "Fall 2021")
        content_split[0] = content_split[0].split(self._semester)[1].strip()

        for line in content_split:
            for word in line.split():
                # in case we get empty lines or some other junk, verify there
                # is actually a month in this line of data
                if word in self.MONTHS:
                    # split the line at the month to separate the flavor text
                    # and the actual day, then rebuild the day
                    split_line: List[str] = line.strip().split(word)
                    key: str = "%s%s" % (word, split_line[1])

                    # if there is a hyphen in the key, then we need to generate a range of dates
                    if '-' in key:
                        for date in self._gen_date_range(key, split_line):
                            self._flavored_dates[date[0]] = date[1]

                    # if there was no hyphen, we can just add the key as necessary
                    else:
                        self._flavored_dates[key] = split_line[0].strip()

                    break

        return

    def _gen_date_range(self, key: str, details: List[str] = [""]) -> Iterator[Tuple[int]]:
        hold_key: List[str] = key.split('-')

        # if there is a month to the right of the hyphen, then we need
        # to gather the rest of the days from this month and the couple
        # of days at the beginning of the next month
        if hold_key[1].split()[0] in self.MONTHS:

            # split the left and right sides of the hyphen
            # ex. November 28-December 1
            left_month: List[str] = hold_key[0].split()
            right_month: List[str] = hold_key[1].split()

            # gather the proper range of days for each of the two months
            for month in [left_month[0], right_month[0]]:
                for (_year, _month, _day, _weekday) in self._calendar \
                .itermonthdays4(int(self._semester.split()[1]), self.MONTHS.index(month)):

                    # since itermonthdays4 does the entire month,
                    # we want to check for if the integer date
                    # is where it needs to be
                    if _day >= int(left_month[1]):
                        yield ("%s %d" % (left_month[0], _day), details[0])
                    elif _day <= int(right_month[1]):
                        yield ("%s %d" % (right_month[0], _day), details[0])

        # if there is no month to the right of hyphen, then we're good
        # to just generate a range
        else:
            for i in range(int(hold_key[0].split()[1]), int(hold_key[1]) + 1):
                yield ("%s %d" % (key.split()[0], i), details[0])

        return

    def _get_meeting_dates(self, meetings) -> None:
        print("%-25s %-30s %10s" % (__name__, currentframe().f_code.co_name, "Filtering Meeting Dates..."))

        semester: List[str] = self._semester.split()
        season: str = semester[0]
        year: int = int(semester[1])

        # the first and last days are needed to tell us when to start and stop adding
        # to the meeting table, respectively
        first_day: str = None
        last_day: str = None
        finals_week: Dict[str, str] = {}

        for key, value in meetings.items():
            if self.FIRST_DAY in value.lower().strip():
                first_day = key
            elif self.LAST_DAY in value.lower().strip():
                last_day = key
            elif self.FINAL_EXAMS in value.lower().strip():
                finals_week[key] = value

        # started will let us know whether or not we should still getting dates
        started: bool = False
        meet_dates: Dict[str] = {}

        # iterate through each month in the given semester, using itermonthdays4.
        # itermonthdays4 returns a tuple structured like so: (year, month, day_of_month, day_of_week).
        for month in self.SEMESTER_MONTHS[season]:
            for (_year, _month, _day, _weekday) in self._calendar.itermonthdays4(year, month):
                # old_key represents the key for the original meetings dict,
                # while new_key is the same thing with the weekday
                old_key: str = "%s %d" % (self.MONTHS[_month - 1], _day)
                new_key: str = "%s, %s" % (self.WEEKDAYS[_weekday], old_key)

                if _month == self.SEMESTER_MONTHS[season][0]:
                    if _day >= int(first_day.split()[1]):
                        started = True
                elif _month == self.SEMESTER_MONTHS[season][-1]:
                    if _day > int(last_day.split()[1]):
                        started = False

                # if the classes are ongoing and we've reached a date with a weekday
                # that this class meets on, create a new slot for it
                if started and _weekday in self._meeting_days:
                    # if meetings.get(old_key):
                    #     meet_dates[new_key] = meetings[old_key]
                    # else:
                    #     meet_dates[new_key] = ""
                    meet_dates[new_key] = meetings[old_key] if meetings.get(old_key) else ""

        # append finals week to the end of the calendar
        for (_year, _month, _day, _weekday) in self._calendar.itermonthdays4(
            year,
            self.SEMESTER_MONTHS[season][-1]
        ):
            key: str = "%s %d" % (self.MONTHS[_month - 1], _day)
            if key in finals_week.keys():
                # if the day is not a weekend...
                if _weekday not in [5, 6]:
                    meet_dates["%s, %s" % (self.WEEKDAYS[_weekday], key)] = finals_week[key]

        return meet_dates

    def _append_weekday(self, year: int, month: int, day: int) -> str:
        for (_year, _month, _day, _weekday) in self._calendar.itermonthdays4(
            year,
            month + 1
        ):
            # avoid spilling out into other months
            if _month != month + 1: continue
            if _day == day:
                return "%s, %s %d" % (self.WEEKDAYS[_weekday], self.MONTHS[_month - 1], _day)

        raise ValueError("Some date (%s %s) wasn't able to be parsed." % (month, day))
