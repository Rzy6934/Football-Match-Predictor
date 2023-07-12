import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

whoscored_url = "https://www.whoscored.com/"


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

def select_year(driver):
    year_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//table[@class="years"]//td[@data-value="2022"]'))
    )
    year_element.click()

def select_month(driver):
    month_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//table[@class="months"]//td[@data-value="7"]'))
    )
    month_element.click()

def get_month_games(driver):
    game_div_elements = driver.find_elements(By.XPATH, '//a[@class="result-1 rc"]')
    
    return game_div_elements

def get_team_names(driver):
    team_names = driver.find_elements(By.XPATH, '//a[@class="team-link"]')
    print(len(team_names))
    home_team = team_names[0].text
    away_team = team_names[1].text
    return home_team, away_team

def get_goals(driver):
    score = driver.find_element(By.XPATH, '//div[@class="score"]')
    splited_score = score.text.split(' ')
    ht_goals = int(splited_score[0])
    at_goals = int(splited_score[2])
    return ht_goals, at_goals

def get_stats(driver):
    ht_shots_element = driver.find_element(By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]')
    at_shots_element = driver.find_element(By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]')
    ht_shots = int(ht_shots_element.text)
    at_shots = int(at_shots_element.text)
    return ht_shots, at_shots


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(whoscored_url)
    accept_cookies(driver)
    select_championship(driver)
    time.sleep(1)
    select_fixtures(driver)
    time.sleep(1)
    select_date_config(driver)
    time.sleep(1)
    select_year(driver)
    time.sleep(1)
    select_month(driver)
    time.sleep(1)
    august_games = get_month_games(driver)
    august_games[0].click()
    home_team, away_team = get_team_names(driver)
    ht_goals, at_goals = get_goals(driver)
    ht_shots, at_shots = get_stats(driver)
    print(home_team, away_team)
    print(ht_goals, at_goals)
    print(ht_shots, at_shots)

    time.sleep(60)