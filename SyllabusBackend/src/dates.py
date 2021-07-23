from bs4 import BeautifulSoup
from bs4.element import ResultSet, NavigableString, Tag
from .colors import Color
from .exceptions import RelErr, RegPDFErr, RegCalErr
from json import dump
from .parsepdf import ParseDates
from .religion import ReligiousObservances
from requests import get as req_get, models
from typing import List, Dict, Tuple

# for testing
from inspect import currentframe

# for cs department,
# if people could make your API exposable and give them a snippet of code# then students could take their class schedule
# merge schedules

# focus now on making religious info and registrar info optional, but make sure dates are set in stone

MARK_BAD_STR: str = "__USELESS__"

class Dates(ParseDates):
    def __init__(self, semester: str, meeting_days: List[int], fall_year: int, spring_year: int):
        self._aux_dates: Dict[str, str] = {}
        self._merged: Dict[str, Dict[str, str]] = {}
        super().__init__(semester, meeting_days, fall_year, spring_year)

        self._aux_build()

    def __iter__(self) -> iter:
        for date in self._merged:
            yield date

        return

    def get_meetings(self) -> List[str]: return self._merged

    def _aux_build(self) -> None:
        self._sort_meetings()
        self._merge_meetings()

        print("%-25s %-30s %5s" % (__name__, currentframe().f_code.co_name, f"{Color.OKCYAN}Done!{Color.ENDC}"))

        return

    def _get_soup(self) -> BeautifulSoup:
        print("%-25s %-30s %10s" % (__name__, currentframe().f_code.co_name, "Retrieving Calendar Page..."))

        url: str = "https://registrar.umbc.edu/%s-undergraduate-academic-calendar/" % self._semester.split()[0].lower()
        page: models.Response = req_get(url)

        if page.status_code != 200: raise RegCalErr(f"{Color.FAIL}Couldn't retrieve academic calendar from Registrar.{Color.ENDC}")

        return BeautifulSoup(page.content, "html.parser")

    def _sort_meetings(self) -> None:
        print("%-25s %-30s %10s" % (__name__, currentframe().f_code.co_name, "Parsing Dates from HTML..."))
        soup: BeautifulSoup = self._get_soup()
        tr_set: ResultSet = soup.find_all("tr")

        # retrieve all tr tags and prepare their td elements for conversion
        first_day: bool = False
        for tr in tr_set:
            td: ResultSet = tr.findAll("td")

            if self.FIRST_DAY in td[1].text.lower():
                first_day = True

            # td[0]: Date in fmt MM/DD/YY
            # td[1]: details pertaining to that date
            if first_day:
                self._convert_date(td[0].text, td[1].text)

        return

    def _convert_date(self, shorthand: str, details: str) -> None:
        lhs: List[str] = shorthand.split('/')
        rhs: List[str] = []

        # sometimes there are extra details in a third column, so we can get those
        if len(lhs) > 3:
            rhs = [lhs[2].split('–')[1].strip(), lhs[3]]

        lhs_month: str = ParseDates.MONTHS[int(lhs[0]) - 1]
        normalized_lhs: str = "%s %s" % (lhs_month, lhs[1])
        normalized_rhs: str = ""

        # anything rhs-related means that there is a hyphen in the date, thus meaning
        # it is a range that needs generation
        if rhs:
            rhs_month: str = ParseDates.MONTHS[int(rhs[0]) - 1]
            normalized_rhs = "%s %s" % (rhs_month if rhs_month != lhs_month else "", rhs[1])

            for date in self._gen_date_range("%s - %s" % (normalized_lhs, normalized_rhs), [details]):
                self._aux_dates[date[0]] = date[1]
        else:
            self._aux_dates[normalized_lhs] = details

        return

    def _merge_meetings(self) -> None:
        print("%-25s %-30s %10s" % (__name__, currentframe().f_code.co_name, "Merging dates from PDF, Calendar Page, and Religious Observances..."))
        # take all dates from the PDF and put them into merged first, since
        # the valid list of class dates was already generated
        for i, (key, value) in enumerate(self._flavored_dates.items()):
            self._merged[key] = {"registrar": "", "religion": ""}
            self._merged[key]["registrar"] = value

        # add all of the dates from the Calendar Page to the merged dict,
        # appending them to what is there if that date is populated, else add a new entry
        for i, (key, value) in enumerate(self._aux_dates.items()):
            # really weird bug here:
            # im unsure if it's an issue with calendar.itermonthdays4() or with the codebase
            # but when passing "August 31" as the raw month value, it gets converted
            # to "July 31" in _append_weekday(). This happens even though every month works
            # perfectly fine. When printing the month passed into the function along
            # with the month value yielded by itermonthdays4, "August" comes out
            # as 7 and 7, even though (month + 1) was fed into itermonthdays4.
            # We'll call this "fixed", but it's something to consider for rewrites.
            # EDIT1: godly recursive call made this consistently work
            # EDIT2: godly recursive call was dogshit
            # EDIT3: itermonthdays4() tries to complete a week by combining months...
            # Man.
            self._loop_merge(i, key, value, "registrar")

        try:
            rel: ReligiousObservances = ReligiousObservances()
            rel_dict: Dict[str, str] = rel.get_observances()

            for i, (key, value) in enumerate(rel_dict.items()):
                self._loop_merge(i, key, value, "religion")
        except RelErr as err:
            print("%-25s %-30s %10s" % (__name__, currentframe().f_code.co_name, err))

        self._sort_dates()

        return

    # with religious, without religious
    # fix typing for value
    def _loop_merge(self, i: int, key: str, value, reg_rel: str) -> None:
        new_key: str = self._append_weekday(
            int(self._semester.split()[1]),
            self.MONTHS.index(key.split()[0]),
            int(key.split()[1])
        )

        if self._merged.get(new_key):
            if self._merged[new_key][reg_rel]:
                if self._merged[new_key][reg_rel].strip().lower() in value.lower():
                    self._merged[new_key][reg_rel] = value
                else:
                    self._merged[new_key][reg_rel] += value
            else:
                self._merged[new_key][reg_rel] = value
        else:
            self._merged[new_key] = {"registrar": "", "religion": ""}
            self._merged[new_key][reg_rel] = value

    # add a couple of blank columns, if they click both and four additional columns then you're adding 5 columns
    # just knowing when it starts should be fine, there may be no need to spread them
    def _sort_dates(self) -> None:
        print("%-25s %-30s %10s" % (__name__, currentframe().f_code.co_name, "Sorting merged dates chronologically..."))

        keys: List[str] = list(self._merged.keys())
        new_merged: Dict[str, Dict[str, str]] = {}

        # bubble sort !!!
        # (this sorts the dates by their month)
        for i in range(len(keys) - 1):
            for j in range(len(keys) - i - 1):
                if self.MONTHS.index(keys[j].split()[1]) > self.MONTHS.index(keys[j + 1].split()[1]):
                    hold: str = keys[j]
                    keys[j] = keys[j + 1]
                    keys[j + 1] = hold

        # another bubble sort !!!1!1
        # (this sorts the sorted-by-month dates by day)
        # may sort outside of months, fix me
        for i in range(len(keys) - 1):
            for j in range(len(keys) - i - 1):
                if self.MONTHS.index(keys[j].split()[1]) == self.MONTHS.index(keys[j + 1].split()[1]):
                    if int(keys[j].split()[2]) > int(keys[j + 1].split()[2]):
                        hold: str = keys[j]
                        keys[j] = keys[j + 1]
                        keys[j + 1] = hold

        # log all dates that are not during meeting days (ex. MW) in aux, along
        # with the index at which they reside
        aux: List[Tuple[int, str]] = []
        for i, key in enumerate(keys):
            if self.WEEKDAYS.index(key.split(',')[0]) not in self._meeting_days:
                aux.append((i, key))

        # this is absolutely going to need some more edgecase checking
        # but i'm hitting a wall with this part of the backend's functionality
        # and would rather revisit it later
        for (i, key) in aux:
            # avoid an out-of-bounds
            if i - 1 >= 0:
                # iterate to the last useful date, then add it to that date's flavoring
                j: int = i
                while self.WEEKDAYS.index(keys[j].split(',')[0]) not in self._meeting_days:
                    j -= 1

                # for both registrar and religion info, insert info on days that the class
                # doesn't meet on the last useful date
                for in_key in ["registrar", "religion"]:
                    if self._merged[key][in_key]:
                        if self._merged[keys[j]][in_key]:
                            self._merged[keys[j]][in_key] += "\n\n%s (%s)" % (self._merged[key][in_key], key)
                        else:
                            self._merged[keys[j]][in_key] += "%s (%s)" % (self._merged[key][in_key], key)

                keys[i] += MARK_BAD_STR

        valid: bool = False

        # chop unnecessary dates off of the front and back
        for i in range(len(keys)):
            if MARK_BAD_STR not in keys[i]:
                if self.FINAL_EXAMS in self._merged[keys[i]]["registrar"].lower():
                    valid = False
                if self.FIRST_DAY in self._merged[keys[i]]["registrar"].lower():
                    if "%s (" % self.FIRST_DAY in self._merged[keys[i]]["registrar"].lower():
                        keys[i] += MARK_BAD_STR
                    valid = True

                if not valid:
                    keys[i] += MARK_BAD_STR

        # if we've appended "__USELESS__" to a date, then it is not within our
        # valid range of meeting dates, thus can be scrapped
        for key in keys:
            if MARK_BAD_STR not in key:
                new_merged[key] = self._merged[key]

        self._merged = new_merged

        return
