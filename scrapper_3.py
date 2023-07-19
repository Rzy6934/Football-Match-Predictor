import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

whoscored_url = "https://www.whoscored.com/"
all_games_data = []


def accept_cookies(driver):
    agree_cookies_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "css-1wc0q5e"))
    )

    agree_cookies_btn.click()

def select_championship(driver, championship):
    championship_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, championship))
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
        EC.element_to_be_clickable((By.XPATH, '//table[@class="years"]//td[@data-value="' + year + '"]'))
    )

    year_element.click()

def select_month(driver, month):
    month_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//table[@class="months"]//td[@data-value="' + month + '"]'))
    )

    month_element.click()

def get_selectable_years(driver):
    years_elements = driver.find_elements(By.CSS_SELECTOR, "table.years td.selectable")
    years = []

    for year_element in years_elements:
        year = year_element.text
        years.append(year)

    return years

def get_selectable_months(driver):
    months_elements = driver.find_elements(By.CSS_SELECTOR, "table.months td.selectable")
    months = []

    for month_element in months_elements:
        month = month_element.get_attribute("data-value").strip()
        months.append(month)

    return months

def get_month_games(driver):
    game_div_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[@class="result-1 rc"]'))
    )

    game_urls = [link.get_attribute("href") for link in game_div_elements]

    return game_urls 

def get_team_names(driver):
    team_names = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[@class="team-link"]'))
    )

    home_team = team_names[0].text
    away_team = team_names[1].text

    return home_team, away_team

def get_game_date(driver):
    game_date_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//dt[text()="Date:"]/following-sibling::dd'))
    )

    game_date_obj = datetime.strptime(game_date_element.text, "%a, %d-%b-%y")
    formatted_game_date = game_date_obj.strftime("%d/%m/%Y")

    return formatted_game_date

def get_goals(driver):
    half_time_score_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//dt[text()="Half time:"]/following-sibling::dd[1]'))
    )
    full_time_score_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//dt[text()="Full time:"]/following-sibling::dd[1]'))
    )

    ht_half_time_goals, at_half_time_goals = half_time_score_element.text.split(":")
    ht_full_time_goals, at_full_time_goals = full_time_score_element.text.split(":")

    game_goals = [int(ht_half_time_goals), int(at_half_time_goals), int(ht_full_time_goals), int(at_full_time_goals)]

    return game_goals

def get_stats(driver):
    ht_shots_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
    )
    at_shots_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'))
    )
    shot_stats_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="toggle-stat-details iconize iconize-icon-right ui-state-transparent-default"]'))
    )
    shot_stats_element.click()
    ht_target_shots_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-for="shotsOnTarget"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
    )
    at_target_shots_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-for="shotsOnTarget"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'))
    )
    ht_possession_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-for="possession"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
    )
    at_possession_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-for="possession"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'))
    )
    ht_pass_success_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-for="passSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
    )
    at_pass_success_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-for="passSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
    )

    game_stats = [int(ht_shots_element.text), int(at_shots_element.text), int(ht_target_shots_element.text), int(at_target_shots_element.text),
                  float(ht_possession_element.text), float(at_possession_element.text), float(ht_pass_success_element.text), float(at_pass_success_element.text)]

    return game_stats

def add_full_time_results(all_games_data):
    if game_data[5] > game_data[6]:
        game_data.insert(7, "H")
    else:
        game_data.insert(7, "NH")

def add_matchday(all_games_data, cpt_starting_value):
    cpt = cpt_starting_value
    for game in all_games_data:
        game.insert(1, (cpt//10)+1)
        cpt += 1


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(whoscored_url)
    accept_cookies(driver)
    # time.sleep(1)
    select_championship(driver, "Serie A")
    # time.sleep(1)
    select_season(driver, "2022/2023")
    # time.sleep(1)
    select_fixtures(driver)
    # time.sleep(1)
    select_date_config(driver)
    # time.sleep(1)
    selectable_years = get_selectable_years(driver)
    time.sleep(1)
    for year in selectable_years[1:2]:
        select_year(driver, year)
        time.sleep(1)
        selectable_months = get_selectable_months(driver)
        print(selectable_months)
        time.sleep(1)
        for month in selectable_months[3:6]:
            select_month(driver, month)
            time.sleep(1)
            month_games = get_month_games(driver)

            for url in month_games:
                driver.execute_script("window.open('');")
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(1)
                driver.get(url)
                time.sleep(1)
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
                # time.sleep(1)
                driver.close()
                # time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])

            month_games = []
                
    add_full_time_results(all_games_data)
    add_matchday(all_games_data, 270)

    json_data = json.dumps(all_games_data)

    with open("data/Serie A/2022-2023/Apr_May_Jun_2023.json", "w") as json_file:
        json_file.write(json_data)

    time.sleep(60)
