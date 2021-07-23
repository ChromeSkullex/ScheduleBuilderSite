from bs4 import BeautifulSoup, ResultSet
from .colors import Color
from .exceptions import RelErr
from requests import get as req_get, models
from typing import Dict, Iterator

# for testing
from inspect import currentframe

class ReligiousObservances:
    def __init__(self):
        self._observances: Dict[str, str] = {}
        self._build()

    def get_observances(self) -> Dict[str, str]:
        return self._observances

    def _build(self) -> None:
        self._parse_observances()
        print("%-25s %-30s %5s" % (__name__, currentframe().f_code.co_name, f"{Color.OKCYAN}Done!{Color.ENDC}"))

        return

    def _get_soup(self) -> BeautifulSoup:
        print("%-25s %-30s %10s" % (__name__, currentframe().f_code.co_name, "Retrieving Observances Page..."))

        url: str = "https://www.american.edu/ocl/kay/major-religious-holy-days.cfm"
        page: models.Response = req_get(url)

        if page.status_code != 200: raise RelErr(f"{Color.FAIL}Failed to merge Religious Observances.{Color.ENDC}")

        return BeautifulSoup(page.content, "html.parser")

    def _parse_observances(self) -> None:
        print("%-25s %-30s %10s" % (__name__, currentframe().f_code.co_name, "Parsing Observances from HTML..."))
        soup: BeautifulSoup = self._get_soup()
        tr_set: ResultSet = soup.find_all("tr")

        for tr in tr_set:
            td: ResultSet = tr.findAll("td")

            # td[0]: month
            # td[1]: day of month
            # td[2]: observance
            # td[3]: religion
            try:
                if td:
                    if '&' in td[1].text:
                        for date in self._spread_observance(td[0].text.strip(), td[1].text.strip()):
                            self._observances[date] = "%s [%s]" % (td[2].text.strip(), td[3].text.strip())
                    else:
                        date: str = "%s %s" % (td[0].text.strip(), td[1].text.strip())
                        self._observances[date] = "%s [%s]" % (td[2].text.strip(), td[3].text.strip())
            except:
                raise RelErr(f"{Color.FAIL}Failed to parse Religious information.{Color.ENDC}")

    def _spread_observance(self, month: str, day: str) -> Iterator[str]:
        # i'm going to need to do some checking for if the month changes here,
        # should be easy
        yield "%s %s" % (month, day.split('&')[0])
        yield "%s %s" % (month, day.split('&')[1])

        return
