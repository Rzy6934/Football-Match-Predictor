import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

whoscored_url = "https://www.whoscored.com/"
months_dico = {"Jan":0, "Feb":1, "Mar":2, "Apr":3, "May":4, "Jun":5, "Jul":6, "Aug":7, "Sep":8, "Oct":9, "Nov":10, "Dec":11}
all_games_data = []


def accept_cookies(driver):
    agree_cookies_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "css-1wc0q5e"))
    )

    agree_cookies_btn.click()

def select_championship(driver):
    championship_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Premier League"))
    )

    championship_link.click()

def select_season(driver, season):
    select_season_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "seasons"))
    )

    select_season = Select(select_season_element)

    for option in select_season.options:
        if season in option.text:
            select_season.select_by_value(option.get_attribute("value"))
            break

def select_fixtures(driver):
    fixtures_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Fixtures"))
    )

    fixtures_link.click()

def select_date_config(driver):
    date_config_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "date-config-toggle-button"))
    )

    date_config_link.click()

def select_year(driver, year):
    year_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//table[@class="years"]//td[@data-value="' + str(year) + '"]'))
    )

    year_element.click()

def select_month(driver, month):
    month_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//table[@class="months"]//td[@data-value="' + str(months_dico[month]) + '"]'))
    )

    month_element.click()

def get_month_games(driver):
    game_div_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[@class="result-1 rc"]'))
    )

    game_urls = [link.get_attribute("href") for link in game_div_elements]

    return game_urls 

def get_team_names(driver):
    team_names = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//a[@class="team-link"]'))
    )

    home_team = team_names[0].text
    away_team = team_names[1].text

    return home_team, away_team

def get_game_date(driver):
    game_date_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//dt[text()="Date:"]/following-sibling::dd'))
    )

    game_date_obj = datetime.strptime(game_date_element.text, "%a, %d-%b-%y")
    formatted_game_date = game_date_obj.strftime("%d/%m/%Y")

    return formatted_game_date

def get_goals(driver):
    half_time_score_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//dt[text()="Half time:"]/following-sibling::dd[1]'))
    )
    full_time_score_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//dt[text()="Full time:"]/following-sibling::dd[1]'))
    )

    ht_half_time_goals, at_half_time_goals = half_time_score_element.text.split(":")
    ht_full_time_goals, at_full_time_goals = full_time_score_element.text.split(":")

    game_goals = [int(ht_half_time_goals), int(at_half_time_goals), int(ht_full_time_goals), int(at_full_time_goals)]

    return game_goals

def get_stats(driver):
    ht_shots_element = driver.find_element(By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]')
    at_shots_element = driver.find_element(By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]')
    shot_stats_element = driver.find_element(By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="toggle-stat-details iconize iconize-icon-right ui-state-transparent-default"]')
    shot_stats_element.click()
    ht_target_shots_element = driver.find_element(By.XPATH, '//li[@data-for="shotsOnTarget"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]')
    at_target_shots_element = driver.find_element(By.XPATH, '//li[@data-for="shotsOnTarget"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]')
    ht_possession_element = driver.find_element(By.XPATH, '//li[@data-for="possession"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]')
    at_possession_element = driver.find_element(By.XPATH, '//li[@data-for="possession"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]')
    ht_pass_success_element = driver.find_element(By.XPATH, '//li[@data-for="passSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]')
    at_pass_success_element = driver.find_element(By.XPATH, '//li[@data-for="passSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]')

    game_stats = [int(ht_shots_element.text), int(at_shots_element.text), int(ht_target_shots_element.text), int(at_target_shots_element.text),
                  float(ht_possession_element.text), float(at_possession_element.text), float(ht_pass_success_element.text), float(at_pass_success_element.text)]

    return game_stats

def add_full_time_results(game_data):
    if game_data[5] > game_data[6]:
        game_data.insert(7, "H")
    else:
        game_data.insert(7, "NH")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(whoscored_url)
    accept_cookies(driver)
    time.sleep(1)
    select_championship(driver)
    time.sleep(1)
    select_season(driver, "2021/2022")
    time.sleep(1)
    select_fixtures(driver)
    time.sleep(1)
    select_date_config(driver)
    time.sleep(1)
    select_year(driver, 2021)
    time.sleep(1)
    select_month(driver, "Aug")
    time.sleep(1)
    month_games = get_month_games(driver)

    for url in month_games[:5]:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(url)
        game_data = []
        game_date = get_game_date(driver)
        home_team, away_team = get_team_names(driver)
        game_goals = get_goals(driver)
        game_stats = get_stats(driver)
        game_data.append(game_date)
        game_data.append(home_team)
        game_data.append(away_team)
        game_data += game_goals
        game_data += game_stats
        all_games_data.append(game_data)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
    for game_data in all_games_data:
        add_full_time_results(game_data)
        
    print(all_games_data)
    time.sleep(60)