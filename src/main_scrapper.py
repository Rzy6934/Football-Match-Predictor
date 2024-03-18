import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service

CHROMEDRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
service = ChromeService(executable_path=CHROMEDRIVER_PATH)
service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")


whoscored_url = "https://www.whoscored.com/"
all_games_data = []
championships_list = ["Ligue 1", "Bundesliga", "Serie A", "Premier League", "LaLiga"]

xpath_stats_elements = {
    "not_clickable_elements":{
        "possession": {
            "home": '//li[@data-for="possession"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
            "away": '//li[@data-for="possession"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
        },
        "cornersTotal": {
            "home": '//li[@data-for="cornersTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
            "away": '//li[@data-for="cornersTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
        }
    },
    "clickable_elements": {
        "shotsTotal": {
            "shotsTotal": {
                "home": '//li[@data-for="shotsTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="shotsTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "shotsOnTarget": {
                "home": '//li[@data-for="shotsOnTarget"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="shotsOnTarget"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "shotsOffTarget": {
                "home": '//li[@data-for="shotsOffTarget"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="shotsOffTarget"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "shotsBlocked": {
                "home": '//li[@data-for="shotsBlocked"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="shotsBlocked"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            }
        },
        "passSuccess": {
            "passesTotal": {
                "home": '//li[@data-for="passesTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="passesTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "passSuccess": {
                "home": '//li[@data-for="passSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="passSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "passesKey": {
                "home": '//li[@data-for="passesKey"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="passesKey"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            }
        },
        "dribblesWon": {
            "dribblesAttempted": {
                "home": '//li[@data-for="dribblesAttempted"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="dribblesAttempted"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "dribblesWon": {
                "home": '//li[@data-for="dribblesWon"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="dribblesWon"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "dribbleSuccess": {
                "home": '//li[@data-for="dribbleSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="dribbleSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            }
        },
        "aerialsWon": {
            "aerialsWon": {
                "home": '//li[@data-for="aerialsWon"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="aerialsWon"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "aerialSuccess": {
                "home": '//li[@data-for="aerialSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="aerialSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "defensiveAerials": {
                "home": '//li[@data-for="defensiveAerials"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="defensiveAerials"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "offensiveAerials": {
                "home": '//li[@data-for="offensiveAerials"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="offensiveAerials"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            }
        },
        "tackleSuccessful": {
            "tacklesTotal": {
                "home": '//li[@data-for="tacklesTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="tacklesTotal"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "tackleSuccessful": {
                "home": '//li[@data-for="tackleSuccessful"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="tackleSuccessful"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "tackleSuccess": {
                "home": '//li[@data-for="tackleSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="tackleSuccess"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "interceptions": {
                "home": '//li[@data-for="interceptions"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="interceptions"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            }
        },
        "dispossessed": {
            "foulsCommited": {
                "home": '//li[@data-for="foulsCommited"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="foulsCommited"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            },
            "offsidesCaught": {
                "home": '//li[@data-for="offsidesCaught"]//div[@class="match-centre-stat-values"]//span[@data-field="home"]',
                "away": '//li[@data-for="offsidesCaught"]//div[@class="match-centre-stat-values"]//span[@data-field="away"]'
            }
        }
    }
}

def accept_cookies(driver):
    try:
        agree_cookies_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-1wc0q5e"))
        )
        agree_cookies_btn.click()
    
    except Exception as e:
        print(f"Failed to accept cookies : {e}")

def close_add_window(driver):
    try:
        add_window_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@style="float: right;"]/svg'))
        )
        add_window_btn.click()
    
    except Exception as e:
        print(f"Failed to close add window : {e}")

def close_webpush_window(driver):
    try:
        webpush_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="webpush-swal2-close"]'))
        )
        webpush_btn.click()
    
    except Exception as e:
        print(f"Failed to close webpush window : {e}")

def scroll_to_stats(driver):
    try:
        stats_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//li[@data-for="dispossessed"]//div[@class="toggle-stat-details iconize iconize-icon-right ui-state-transparent-default"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", stats_element)
    
    except Exception as e:
        print(f"Failed to scroll to stats : {e}")


def select_championship(driver, championship):
    try:
        top_tournaments_button = WebDriverWait(driver,10).until(
          EC.element_to_be_clickable((By.ID, "Top-Tournaments-btn"))
        )
        top_tournaments_button.click()
        
        championship_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, championship))
        )
        championship_link.click()
    
    except Exception as e:
        print(f"Failed to select the champiionship : {e}")

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

    except Exception as e:
        print(f"Failed to select the season : {e}")
        
def select_stage(driver, championship):
    try:
        select_stage_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "stages"))
        )
        select_stage = Select(select_stage_element)
        
        for option in select_stage.options:
            if championship in option.text:
                select_stage.select_by_value(option.get_attribute("value"))
                break
            
    except Exception as e:
        print(f"Failed to select the season : {e}")

def select_fixtures(driver):
    try:
        fixtures_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Fixtures"))
        )
        fixtures_link.click()

    except Exception as e:
        print(f"Failed to select the fixtures : {e}")

def select_date_config(driver):
    try:
        date_config_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "date-config-toggle-button"))
        )
        date_config_link.click()
    
    except Exception as e:
        print(f"Failed to select the date configuration : {e}")

def select_year(driver, year):
    try:
        year_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//table[@class="years"]//td[@data-value="' + year + '"]'))
        )
        year_element.click()
    
    except Exception as e:
        print(f"Failed to select the year : {e}")

def select_month(driver, month):
    try:
        month_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//table[@class="months"]//td[@data-value="' + month + '"]'))
        )
        month_element.click()

    except Exception:
        print(f"Failed to select the month : {e}")

def get_selectable_years(driver):
    try:
        years_elements = driver.find_elements(By.CSS_SELECTOR, "table.years td.selectable")
        years = []

        for year_element in years_elements:
            year = year_element.text
            years.append(year)
    
    except Exception as e:
        print(f"Failed to get the selectable years : {e}")

    finally:
        return years

def get_selectable_months(driver):
    try:
        months_elements = driver.find_elements(By.CSS_SELECTOR, "table.months td.selectable")
        months = []

        for month_element in months_elements:
            month = month_element.get_attribute("data-value").strip()
            months.append(month)

    except Exception as e:
        print(f"Failed to get the selectable months : {e}")

    finally:
        return months

def get_month_games_url(driver):
    try:
        game_div_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="result-1 rc"]'))
        )

        game_urls = [link.get_attribute("href") for link in game_div_elements]
    
    except Exception as e:
        print(f"Failed to get the urls : {e}")


    finally:
        return game_urls 

def get_team_names(driver):
    try:
        team_names = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="team-link"]'))
        )

        home_team, away_team = team_names[0].text, team_names[1].text
        # print(home_team, away_team)

    except Exception as e:
        print(f"Failed to get the teams names : {e}")
    
    finally:
        return home_team, away_team

def get_game_date(driver):
    try:
        game_date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//dt[text()="Date:"]/following-sibling::dd'))
        )

        game_date_obj = datetime.strptime(game_date_element.text, "%a, %d-%b-%y")
        formatted_game_date = game_date_obj.strftime("%d/%m/%Y")

    except Exception as e:
        print(f"Failed to get the game date : {e}")

    finally:
        return formatted_game_date

def get_goals(driver):
    try:
        try:
            half_time_score_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//dt[text()="Half time:"]/following-sibling::dd[1]'))
            )
            home_team_half_time_goals, away_team_half_time_goals = half_time_score_element.text.split(":")

        except NoSuchElementException:
            home_team_half_time_goals = away_team_half_time_goals = "ND"
        
        full_time_score_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//dt[text()="Full time:"]/following-sibling::dd[1]'))
        )
        home_team_full_time_goals, away_team_full_time_goals = full_time_score_element.text.split(":")

        # print(half_time_score_element.text.split(":"))
        # print(full_time_score_element.text.split(":"))
        
        if home_team_half_time_goals == away_team_half_time_goals == "ND":
            game_goals = [home_team_half_time_goals, away_team_half_time_goals, int(home_team_full_time_goals), int(away_team_full_time_goals)]

        else:
            game_goals = [int(home_team_half_time_goals), int(away_team_half_time_goals), int(home_team_full_time_goals), int(away_team_full_time_goals)]

    except Exception as e:
        print(f"Failed to get game goals : {e}")

    finally:
        return game_goals
    
def get_stat_element(driver, xpath):
    try:
        return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    except Exception as e:
        print(f"Element not found for xpath : {xpath}")
        return None    

def get_stats(driver):
    try:
        game_stats = []

        for category, sub_category_dict in xpath_stats_elements.items():
            if category == "not_clickable_elements":
                for sub_category, stat_xpath_dict in sub_category_dict.items():
                    for stat_key, stat_xpath in stat_xpath_dict.items():
                        stat_element = get_stat_element(driver, stat_xpath)
                        if sub_category == "possession":
                            game_stats.append(float(stat_element.text))
                        else:
                            game_stats.append(int(stat_element.text))

            else:
                for index, (sub_category, stat_xpath_dict) in enumerate(sub_category_dict.items()):
                    try:
                        main_stat_element = get_stat_element(driver, f'//li[@data-for="{sub_category}"]//div[@class="toggle-stat-details iconize iconize-icon-right ui-state-transparent-default"]')
                        if index == 0:
                            main_stat_element.click()
                        else:
                            main_stat_element.click()
                            main_stat_element.click()

                        for stat_key, sub_stat_xpath_dict in stat_xpath_dict.items():
                            try:
                                for sub_stat_key, sub_stat_xpath  in sub_stat_xpath_dict.items():
                                    stat_element = get_stat_element(driver, sub_stat_xpath)
                                    if "Success" in stat_key and "Successful" not in stat_key:
                                        game_stats.append(float(stat_element.text))
                                    else:
                                        game_stats.append(int(stat_element.text))

                            except Exception as e:
                                print(f"Failed to get game stats for {stat_key} : {e}")

                    except Exception as e:
                        print(f"Failed to get main stat element for {stat_key} : {e}")

    except Exception as e:
        print(f"Failed to get all game stats : {e}")
        game_stats = []

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
            if championship_input in championships_list:
                break
            else:
                print("Invalid championship. Please enter a valid championship.")
        
        season_input = input("Season (Follow format YYYY/YYYY) : ")
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

        # driver = webdriver.Chrome(service=service, options=options)
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(whoscored_url)
        accept_cookies(driver)
        close_webpush_window(driver)
        select_championship(driver, championship_input)
        select_season(driver, season_input)
        select_stage(driver, championship_input)
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
                    scroll_to_stats(driver)
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

        # with open(f"configs/{config_championships_dico[championship_input]}", 'w') as configfile:
        #     config.write(configfile)

        json_data = json.dumps(all_games_data)

        with open(f"data/{championship_input}/{season_formatted}/{json_file_name}.json", "w") as json_file:
            json_file.write(json_data)

        time.sleep(5)

    except Exception as e:
        print(f"An error has occurred : {e}")
