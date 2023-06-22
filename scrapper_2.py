import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ligue_1_url = "https://www.ligue1.fr"
cookies_agree_button_id = "didomi-notice-agree-button"
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
    if parts[2] in months_dico:
        parts[2] = str(months_dico[parts[2]])
    for part in parts[1:4]:
        part_formatted = part.zfill(2) if len(part) == 1 else part
        formatted_parts.append(part_formatted)
    return "/".join(formatted_parts)


def format_team_name(team_name):
    parts = team_name.split("-")
    formatted_parts = [part.upper() if len(part) == 2 else part.capitalize() for part in parts]
    return ' '.join(formatted_parts)


def accept_cookies(driver):
    cookies_agree_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, cookies_agree_button_id))
    )
    cookies_agree_button.click()


def get_games_ids(driver):
    games_list = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "match-result"))
    )
    games_id_list = [game.get_attribute("id").split("_")[0] for game in games_list]
    return games_id_list


def get_game_sheet_data(driver, game_id):
    game_sheet_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.clubs-container[href="/feuille-match?matchId=' + game_id + '"]'))
    )
    game_sheet_element.click()
    time.sleep(1)  # Consider using explicit wait instead of fixed sleep

    date_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.MatchHeader-text.uppercase"))
    )
    date = format_datetime(date_element.text)

    home_team_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.MatchHeader-club.team.home a"))
    )
    home_team_href = home_team_element.get_attribute("href")
    home_team = format_team_name(home_team_href.split("=")[-1])

    away_team_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.MatchHeader-club.team.away a"))
    )
    away_team_href = away_team_element.get_attribute("href")
    away_team = format_team_name(away_team_href.split("=")[-1])

    score_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.MatchHeader-scoreResult"))
    )
    home_ft_goals, away_ft_goals = score_element.text.split("-")

    stats_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "nav-title-matchpage-stats"))
    )
    stats_element.click()
    time.sleep(1)  # Consider using explicit wait instead of fixed sleep

    offense_stats_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Attaque"))
    )
    offense_stats_element.click()
    time.sleep(1)  # Consider using explicit wait instead of fixed sleep

    td_elements = driver.find_elements(By.CSS_SELECTOR, "td.Opta-Outer")
    offense_stats_list = [element.text for element in td_elements if element.text]
    driver.back()
    driver.back()

    return [date, home_team, away_team, home_ft_goals, away_ft_goals] + offense_stats_list[2:6]


def scrape_ligue1_data():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(ligue_1_url)

    accept_cookies(driver)

    results_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@title="Calendrier/Résultats"]'))
    )
    results_element.click()
    time.sleep(1)  # Consider using explicit wait instead of fixed sleep

    icon_left_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "Icon-chevron-left"))
    )
    for _ in range(6):
        icon_left_element.click()
        time.sleep(1)  # Consider using explicit wait instead of fixed sleep

    games_data_list = []

    for val in range(1):
        gameday_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@data-slick-index="' + str(val) + '"]'))
        )
        gameday_element.click()
        time.sleep(1)  # Consider using explicit wait instead of fixed sleep

        games_id_list = get_games_ids(driver)
        print(games_id_list)

        for game_id in games_id_list:
            game_data = get_game_sheet_data(driver, game_id)
            games_data_list.append([val + 1] + game_data)

        games_id_list = []

        driver.execute_script("window.scrollTo(0, 0);")

    driver.quit()
    print(games_data_list)


scrape_ligue1_data()
