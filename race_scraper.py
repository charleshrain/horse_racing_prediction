"""Helper module used to scrapa future race characteristics"""
import pandas as pd


class RaceInfoScraper:
    """Web scraper for upcoming races"""

    driver = None

    def __init__(self, driver):
        self.driver = driver

    def scrape_race_info(self):
        """Scrapes race categorical info"""

        self.driver.get('https://www.atg.se/spel/V75')
        self.driver.refresh()
        self.driver.maximize_window()
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        races = pd.DataFrame(columns=['race', 'class', 'distance', 'start'])

        for i in range(1, 8):
            try:
                klass = self.decide_class(
                    self.driver.find_element_by_xpath("(//span[@class='race-name'])[" + str(i) + "]").get_attribute(
                        "innerHTML"))
            except Exception as exc:
                print(exc)
                klass = "Other"
            try:
                distans = self.decide_distance(self.driver.find_element_by_xpath(
                    "(//span[@data-test-id='startlist-header-race-info'])[" \
                    + str(i) + "]").get_attribute("innerHTML"))
            except Exception as exc:
                print(exc)
                distans = "M"

            startmode = "A" if "Auto" in self.driver.find_element_by_xpath(
                "(//span[@data-test-id='startlist-header-race-info'])[" \
                + str(i) + "]").get_attribute(
                "innerHTML") else "V"
            races.loc[i] = [i, klass, distans, startmode]

        races.distance = races.distance.fillna("'M'")  # quick fix
        races['class'].values[races['class'].values == 'Other'] = "'%%'"  # quick fix
        return races

    def decide_class(self, data):
        """Decides race class from description"""
        data = str(data).lower().replace(" ", "")

        classes = {'bronsdivisionen': "'B'",
                   'dubbelklasslopp': "'D'",
                   'elitlopp': "'E'",
                   'flerklasslopp': "'F'",
                   'gulddivisionen': "'G'",
                   'kallblod': "'K'",
                   'klass1': "'1'",
                   'klassi,': "'1'",
                   'klass2': "'2'",
                   'klassii,': "'2'",
                   'rlingslopp': "'L'",
                   'silverdivisionen': "'S'",
                   'stodivisionen': "'Q'",
                   'stoeliten': "'X'",
                   'diamant': "'X'",
                   'utomv5': "'U'",
                   'Vv5lopp': "'V'"}

        for classkey, symbol in classes.items():
            if classkey in data:
                return symbol
        return "'%%'"

    def decide_distance(self, data):
        """Decides distance from description"""
        data = str(data).lower().replace(" ", "")

        distances = {'1640': "'K'",
                     '1650': "'K'",
                     '1609': "'K'",
                     '2100': "'M'",
                     '2140': "'M'",
                     '2175': "'M'",
                     '2300': "'M'",
                     '2550': "'L'",
                     '2609': "'L'",
                     '2640': "'L'",
                     '2700': "'S'",
                     '2850': "'S'",
                     '3140': "'S'",
                     '3160': "'S'",
                     '4000': "'S'"}

        for distkey, symbol in distances.items():
            if distkey in data and symbol is not None:
                return symbol
        return 'M'
