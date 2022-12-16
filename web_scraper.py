"""Webscraper for race participant data"""
import pandas as pd

class WebScraper:
    """Web scraper class"""
    Counter = 1

    driver = None

    def __init__(self, driver):
        self.driver = driver

    def inc_couter(self):
        """Increments counter variable"""
        WebScraper.counter = WebScraper.Counter + 1
        return WebScraper.Counter - 1

    def calc_win_cur(self, wins_string):
        """calculate win percentage in current year"""
        wins_split = wins_string.split('-')

        if len(wins_split[0]) == 3:
            if float(wins_split[0][0:2]) != 0:
                return round(100 * float(wins_split[0][2]) / float(wins_split[0][0:2]))
        if len(wins_split[0]) == 4:
            if float(wins_split[0][:1]) != 0:
                return round(100 * float(wins_split[0][2:]) / float(wins_split[0][:1]))
        if len(wins_split[0]) == 2:
            if float(wins_split[0][0]) != 0:
                return round(100 * float(wins_split[0][1:]) / float(wins_split[0][0]))
        return 0

    def scrape_race_data(self):
        """Scrapes data"""

        self.driver.get('https://www.atg.se/spel/V75')  # go to race start page
        self.driver.refresh()
        self.driver.maximize_window()

        # click customize stats button
        self.driver.find_element_by_css_selector(
            'button.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.MuiButton-outlinedPrimary.MuiButton-sizeMedium.MuiButton-outlinedSizeMedium.MuiButton-root.MuiButton-outlined.MuiButton-outlinedPrimary.MuiButton-sizeMedium.MuiButton-outlinedSizeMedium.css-i42r0d.css-1ba6utu').click()

        # clear selected stats button
        self.driver.find_element_by_class_name('css-tqseha-Button-styles--root-Button--Button').click()

        # check stats checkboxes
        # money
        self.driver.find_elements_by_css_selector('span.css-1hngy38-Checkbox-styles--label')[1].click()
        # win percent
        self.driver.find_elements_by_css_selector('span.css-1hngy38-Checkbox-styles--label')[2].click()
        # points
        self.driver.find_elements_by_css_selector('span.css-1hngy38-Checkbox-styles--label')[17].click()
        # place percentage
        self.driver.find_elements_by_css_selector('span.css-1hngy38-Checkbox-styles--label')[15].click()
        # races this year
        self.driver.find_elements_by_css_selector('span.css-1hngy38-Checkbox-styles--label')[19].click()

        # click save selected stats button
        self.driver.find_element_by_css_selector("button[data-test-id='save-startlist-options']").click()

        # read upcoming 7 races data into dataframe
        upcoming = pd.DataFrame()
        for i in range(1, 8):

            path = f"(//table[@data-test-id='startlist-race-{i}'])"
            df0 = pd.read_html(self.driver.find_element_by_xpath(path).get_attribute("outerHTML"))[0]
            df0['Lopp'] = i
            if 'Ryttare' in df0.columns:
                df0.rename(columns={'Ryttare': 'Kusk'}, inplace=True)
            df0 = df0[~df0['Kusk'].str.contains('Tillägg')]
            df0['track'] = df0['Lopp'].index + 1
            upcoming_temp = pd.concat([upcoming, df0])
            upcoming = upcoming_temp

        upcoming.drop(upcoming.columns[[0, 1, 8]], axis=1, inplace=True)

        upcoming.columns = ['betp', 'money', 'winp', 'points', 'placep', 'wincur', 'race', 'track']

        upcoming['betp'] = upcoming['betp'].map(
            lambda x: x.lstrip('+-').rstrip('%'))
        upcoming['winp'] = upcoming['winp'].map(
            lambda x: x.lstrip('+-').rstrip('%'))
        upcoming['placep'] = upcoming['placep'].map(
            lambda x: x.lstrip('+-').rstrip('%'))
        upcoming['wincur'] = upcoming['wincur'].map(
            lambda x: WebScraper.calc_win_cur(self, x))
        upcoming['money'] = [float(str(val).replace(' ', '').replace(',', '.')) for val in upcoming['money'].values]
        upcoming['points'] = upcoming['points'].fillna(0)  # quick fix

        return upcoming
