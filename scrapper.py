import time
from selenium import webdriver
from selenium.webdriver.common.by import By


################################
# VARIABLES
################################
ligue_1_url = "https://www.ligue1.fr"
cookies_agree_button_id = "didomi-notice-agree-button"
games_id_list = []
games_data_list = []
offense_stats_list = []
months_dico = {
    "JANVIER": 1,
    "FÉVRIER": 2,
    "MARS": 3,
    "AVRIL": 4,
    "MAIL": 5,
    "JUIN": 6,
    "JUILLET": 7,
    "AOÛT": 8,
    "SEPTEMBRE": 9,
    "OCTOBRE": 10,
    "NOVEMBRE": 11,
    "DÉCEMBRE": 12
}

################################
# FUNCTIONS
################################
def format_datetime(datetime):
    parts = datetime.split(" ")
    formatted_parts = []
    if parts[2] in months_dico.keys():
        parts[2] = str(months_dico[parts[2]])
    for part in parts[1:4]:
        if len(part) == 1:
            part_formatted = part.zfill(2)
            formatted_parts.append(part_formatted)
        else:
            formatted_parts.append(part)
    
    return "/".join(formatted_parts)

def format_team_name(team_name):
    parts = team_name.split("-")
    formatted_parts = []
    for part in parts:
        if len(part) == 2:
            formatted_parts.append(part.upper())
        else:
            formatted_parts.append(part.capitalize())

    return ' '.join(formatted_parts)

def get_games_ids():
    games_list = driver.find_elements(By.CLASS_NAME, "match-result")
    for game in games_list:
        games_id_list.append(game.get_attribute("id").split("_")[0])
    games_list = []


################################
# MAIN PROGRAM
################################

# Connection to the main page of the Ligue 1 website
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(ligue_1_url)


# Click the button to accept cookies
cookies_agree_button = driver.find_element(By.ID, cookies_agree_button_id)
if cookies_agree_button.is_displayed() and cookies_agree_button.is_displayed:
    cookies_agree_button.click()


# Click on the link to go to the Calendar/Results page
results_element = driver.find_element(By.XPATH, '//a[@title="Calendrier/Résultats"]')
if results_element.is_enabled() and results_element.is_displayed:
    results_element.click()
    time.sleep(1)


# Click on the left chevron to scroll down to the first championship day  
icon_left_element = driver.find_element(By.CLASS_NAME, "Icon-chevron-left")
if icon_left_element.is_enabled() and icon_left_element.is_displayed():
    for i in range(0, 6):
        icon_left_element.click()
        time.sleep(1)

# Course of each championship day
for val in range(0,2):
    
    gameday_element = driver.find_element(By.XPATH, '//a[@data-slick-index="' + str(val) + '"]')
    if gameday_element.is_enabled() and gameday_element.is_displayed():
        gameday_element.click()
        time.sleep(1)
        games_list = driver.find_elements(By.CLASS_NAME, 'match-result')
        
        for game in games_list:
            games_id_list.append(game.get_attribute("id").split("_")[0])
        
        print(games_id_list)
        
        for id in games_id_list:
            game_sheet_element = driver.find_element(By.CSS_SELECTOR, 'a.clubs-container[href="/feuille-match?matchId='+id+'"]')
            if game_sheet_element.is_enabled() and game_sheet_element.is_displayed():
                game_sheet_element.click()
                time.sleep(1)
                
            date_element = driver.find_element(By.CSS_SELECTOR, "p.MatchHeader-text.uppercase")
            date = format_datetime(date_element.text)

            home_team_element = driver.find_element(By.CSS_SELECTOR, "div.MatchHeader-club.team.home a")
            home_team_href = home_team_element.get_attribute("href")
            home_team = format_team_name(home_team_href.split("=")[-1])

            away_team_element = driver.find_element(By.CSS_SELECTOR, "div.MatchHeader-club.team.away a")
            away_team_href = away_team_element.get_attribute("href")
            away_team = format_team_name(away_team_href.split("=")[-1])

            score_element = driver.find_element(By.CSS_SELECTOR, "p.MatchHeader-scoreResult")
            home_ft_goals, away_ft_goals = score_element.text.split("-")
            
            stats_element = driver.find_element(By.ID, "nav-title-matchpage-stats")
            if stats_element.is_enabled() and stats_element.is_displayed():
                stats_element.click()
                time.sleep(1)
                offense_stats_element = driver.find_element(By.LINK_TEXT, "Attaque")
                
                if offense_stats_element.is_enabled() and offense_stats_element.is_displayed():
                    offense_stats_element.click()
                    time.sleep(1)

                    td_elements = driver.find_elements(By.CSS_SELECTOR, "td.Opta-Outer")
                    for element in td_elements:
                        if len(element.text) > 0:
                            offense_stats_list.append(element.text)
                    
                    games_data_list.append([val+1, date, home_team, away_team, home_ft_goals, away_ft_goals, offense_stats_list[2], offense_stats_list[3], offense_stats_list[4], offense_stats_list[5]])
                    
                    td_elements = []
                    offense_stats_list = []
                
                driver.back()
                driver.back()
        games_id_list = []
    
    driver.execute_script("window.scrollTo(0, 0);")
        
driver.quit()
print(games_data_list)
