import time
import json
import configparser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


config = configparser.ConfigParser()

whoscored_url = "https://www.whoscored.com/"
all_games_data = []
config_championships_dico = {
    "Premier League": "config_EN.ini", 
    "LaLiga": "config_ES.ini", 
    "Serie A": "config_IT.ini", 
    "Bundesliga": "config_DE.ini", 
    "Ligue 1": "config_FR.ini"
}

def accept_cookies(driver):
    try:
        agree_cookies_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-1wc0q5e"))
        )
        agree_cookies_btn.click()
    
    except Exception:
        print("Failed to accept cookies")

def select_championship(driver, championship):
    try:
        championship_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, championship))
        )
        championship_link.click()
    
    except Exception:
        print("Failed to select the champiionship")

def select_season(driver, season):
    try:
        select_season_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "seasons"))
        )
        select_season = Select(select_season_element)

        for option in select_season.options:
            if season in option.text:
                select_season.select_by_value(option.get_attribute("value"))
                break

    except Exception:
        print("Failed to select the season")

def select_fixtures(driver):
    try:
        fixtures_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Fixtures"))
        )
        fixtures_link.click()

    except Exception:
        print("Failed to select the fixtures")

def select_date_config(driver):
    try:
        date_config_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "date-config-toggle-button"))
        )
        date_config_link.click()
    
    except Exception:
        print("Failed to select the date configuration")

def select_year(driver, year):
    try:
        year_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//table[@class="years"]//td[@data-value="' + year + '"]'))
        )
        year_element.click()
    
    except Exception:
        print("Failed to select the year")

def select_month(driver, month):
    try:
        month_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//table[@class="months"]//td[@data-value="' + month + '"]'))
        )
        month_element.click()

    except Exception:
        print("Failed to select the month")

def get_selectable_years(driver):
    try:
        years_elements = driver.find_elements(By.CSS_SELECTOR, "table.years td.selectable")
        years = []

        for year_element in years_elements:
            year = year_element.text
            years.append(year)
    
    except Exception:
        print("Failed to get the selectable years")

    finally:
        return years

def get_selectable_months(driver):
    try:
        months_elements = driver.find_elements(By.CSS_SELECTOR, "table.months td.selectable")
        months = []

        for month_element in months_elements:
            month = month_element.get_attribute("data-value").strip()
            months.append(month)

    except Exception:
        print("Failed to get the selectable months")

    finally:
        return months

def get_month_games_url(driver):
    try:
        game_div_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="result-1 rc"]'))
        )

        game_urls = [link.get_attribute("href") for link in game_div_elements]
    
    except Exception:
        print("Failed to get the urls")


    finally:
        return game_urls 

def get_team_names(driver):
    try:
        team_names = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="team-link"]'))
        )

        home_team, away_team = team_names[0].text, team_names[1].text

    except Exception:
        print("Failed to get the teams names")
    
    finally:
        return home_team, away_team

def get_game_date(driver):
    try:
        game_date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//dt[text()="Date:"]/following-sibling::dd'))
        )

        game_date_obj = datetime.strptime(game_date_element.text, "%a, %d-%b-%y")
        formatted_game_date = game_date_obj.strftime("%d/%m/%Y")

    except Exception:
        print("Failed to get the game date")

    finally:
        return formatted_game_date

def get_goals(driver):
    try:
        half_time_score_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//dt[text()="Half time:"]/following-sibling::dd[1]'))
        )
        full_time_score_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//dt[text()="Full time:"]/following-sibling::dd[1]'))
        )

        home_team_half_time_goals, away_team_half_time_goals = half_time_score_element.text.split(":")
        home_team_full_time_goals, away_team_full_time_goals = full_time_score_element.text.split(":")

        game_goals = [int(home_team_half_time_goals), int(away_team_half_time_goals), int(home_team_full_time_goals), int(away_team_full_time_goals)]

    except Exception:
        print("Failed to get game goals")

    finally:
        return game_goals

def get_stats(driver):
    try:
        shot_stats_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="toggle-stat-details iconize iconize-icon-right ui-state-transparent-default"]'))
        )
        shot_stats_element.click()
        home_team_total_shots_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
        )
        away_team_total_shots_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="shotsTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'))
        )
        home_team_target_shots_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="shotsOnTarget"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
        )
        away_team_target_shots_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="shotsOnTarget"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'))
        )
        home_team_possession_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="possession"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
        )
        away_team_possession_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="possession"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'))
        )
        home_team_pass_success_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="passSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
        )
        away_team_pass_success_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="passSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'))
        )
        home_team_dribbles_won_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="dribblesWon"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
        )
        away_team_dribbles_won_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="dribblesWon"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'))
        )
        home_team_dribbles_success_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="dribbleSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]'))
        )
        away_team_dribbles_success_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-for="dribbleSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'))
        )

        game_stats = [int(home_team_total_shots_element.text), int(away_team_total_shots_element.text), int(home_team_target_shots_element.text), int(away_team_target_shots_element.text),
                    float(home_team_possession_element.text), float(away_team_possession_element.text), float(home_team_pass_success_element.text), float(away_team_pass_success_element.text)]

    except Exception:
        print("Failed to get game stats")

    finally:
        return game_stats

def get_year_index(season, year):
    parts = season.split("/")
    if year in parts:
        return parts.index(year)
    
def transform_season_format(season):
    parts = season.split("/")
    return f"{parts[0]}-{parts[1]}"
    

if __name__ == "__main__":
    try:
        while True:
            championship_input = input("Championship : ")
            if championship_input in list(config_championships_dico.keys()):
                break
            else:
                print("Invalid championship. Please enter a valid championship.")
        
        config.read(f"configs/{config_championships_dico[championship_input]}")
        season_input = config["Parameters"]["Season"]
        season_formatted = transform_season_format(season_input)
        
        valid_years = season_input.split("/")
        while True:
            year_input = input(f"Year {valid_years[0]} or {valid_years[1]}: ")
            if year_input in valid_years:
                break
            else:
                print("Invalid year. Please enter a valid year.")

        year_index = get_year_index(season_input, year_input)

        while True:
            month_index = int(input("Month : "))
            if  0 <= month_index <= 5:
                break
            else:
                print("Invalid month index. Please enter a number between 0 and 5.")
        
        while True:
            months_range = int(input("Months range : "))
            if 1 <= months_range <= 6:
                break
            else:
                print("Invalid months range. Please enter a number between 1 and 6.")
        
        json_file_name = input("Json File Name : ")

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(whoscored_url)
        accept_cookies(driver)
        select_championship(driver, championship_input)
        select_season(driver, season_input)
        select_fixtures(driver)
        select_date_config(driver)
        selectable_years = get_selectable_years(driver)
        for year in selectable_years[year_index:year_index+1]:
            select_year(driver, year)
            selectable_months = get_selectable_months(driver)
            for month in selectable_months[month_index:month_index+months_range]:
                select_month(driver, month)
                time.sleep(1)
                month_games = get_month_games_url(driver)

                for url in month_games:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
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
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                month_games = []

        with open(f"configs/{config_championships_dico[championship_input]}", 'w') as configfile:
            config.write(configfile)

        json_data = json.dumps(all_games_data)

        with open(f"data/{championship_input}/{season_formatted}/{json_file_name}.json", "w") as json_file:
            json_file.write(json_data)

        time.sleep(5)

    except Exception as e:
        print("An error has occurred : " + str(e))
