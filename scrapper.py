import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome()

ligue_1_url = "https://www.ligue1.fr"
cookies_agree_button_id = "didomi-notice-agree-button"
games_id_list = []
games_data_list = []
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

# Connexion à la page principale du site de la ligue 1
driver.get(ligue_1_url)


# Click sur le bouton permettant d'accepter les cookies
cookies_agree_button = driver.find_element(By.ID, cookies_agree_button_id)
if cookies_agree_button.is_displayed() and cookies_agree_button.is_displayed:
    cookies_agree_button.click()


# Click sur le lien permettant d'accéder à la page du Calendrier/Résultats
results_element = driver.find_element(By.XPATH, '//a[@title="Calendrier/Résultats"]')
if results_element.is_enabled() and results_element.is_displayed:
    results_element.click()
    time.sleep(1)


# Click sur le chevron gauche pour défiler les journées jusqu'à la première journée    
icon_left_element = driver.find_element(By.CLASS_NAME, "Icon-chevron-left")
if icon_left_element.is_enabled() and icon_left_element.is_displayed():
    for i in range(0, 6):
        icon_left_element.click()
        time.sleep(1)

# Parcours de chaque journée
for val in range(0,1):
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
            games_data_list.append([val+1, date, home_team, away_team, home_ft_goals, away_ft_goals])
            driver.back()
        games_id_list = []
    driver.execute_script("window.scrollTo(0, 0);")
        
driver.quit()
print(games_data_list)

# matchs_list = driver.find_elements(By.CLASS_NAME, 'match-result')
# for match in matchs_list:
#     # print(match.get_attribute('id').split('_')[0])
#     match_id_list.append(match.get_attribute('id').split('_')[0])

# print(match_id_list)


# link_game_1 = driver.find_element(By.CSS_SELECTOR, 'a.clubs-container[href="/feuille-match?matchId=70764"]')
# if link_game_1.is_enabled() and link_game_1.is_displayed:
#     print("Link is clickable")
#     link_game_1.click()
# else:
#     print("Link is not clickable")

# date_element = driver.find_element(By.CSS_SELECTOR, "p.MatchHeader-text.uppercase")
# date = format_datetime(date_element.text)

# home_team_element = driver.find_element(By.CSS_SELECTOR, "div.MatchHeader-club.team.home a")
# home_team_href = home_team_element.get_attribute("href")
# home_team = format_team_name(home_team_href.split("=")[-1])

# away_team_element = driver.find_element(By.CSS_SELECTOR, "div.MatchHeader-club.team.away a")
# away_team_href = away_team_element.get_attribute("href")
# away_team = format_team_name(away_team_href.split("=")[-1])

# score_element = driver.find_element(By.CSS_SELECTOR, "p.MatchHeader-scoreResult")
# home_ft_goals, away_ft_goals = score_element.text.split("-")

# print(date)
# print(home_team)
# print(away_team)
# print(home_ft_goals)
# print(away_ft_goals)

    

# stats_game_1 = driver.find_element(By.ID, 'nav-title-matchpage-stats')
# if stats_game_1.is_enabled() and stats_game_1.is_displayed:
#     print("Link is clickable")
#     stats_game_1.click()
# else:
#     print("Link is not clickable")

# link_elements = driver.find_elements(By.TAG_NAME, "a")
# for element in link_elements:
#     if element.text == "Attaque":
#         element.click()
# time.sleep(10)


# class_journees = "js-Scorebar-journeyItem Scorebar-journeyItem slick-slide slick-active"