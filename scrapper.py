import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

ligue_1_url = "https://www.ligue1.fr"

cookies_agree_button_id = "didomi-notice-agree-button"

match_id_list = []

driver.get(ligue_1_url)
cookies_agree_button = driver.find_element(By.ID, cookies_agree_button_id)
cookies_agree_button.click()

link_resultats = driver.find_element(By.XPATH, '//a[@title="Calendrier/Résultats"]')
if link_resultats.is_enabled() and link_resultats.is_displayed:
    print("Link is clickable")
    link_resultats.click()
    time.sleep(1)
else:
    print("Link is not clickable")
    
    
icon_left = driver.find_element(By.CLASS_NAME, "Icon-chevron-left")
if icon_left.is_enabled() and icon_left.is_displayed():
    print("Icon left is clickable")
    for i in range(0, 6):
        icon_left.click()
        time.sleep(1)
    time.sleep(2)
else:
    print("Icon is not clickable")
    

link_j1 = driver.find_element(By.XPATH, '//a[@data-slick-index="0"]')
if link_j1.is_enabled() and link_j1.is_displayed:
    print("Link is clickable")
    link_j1.click()
    time.sleep(1)
else:
    print("Link is not clickable")
    
matchs_list = driver.find_elements(By.CLASS_NAME, 'match-result')
for match in matchs_list:
    # print(match.get_attribute('id').split('_')[0])
    match_id_list.append(match.get_attribute('id').split('_')[0])

link_game_1 = driver.find_element(By.CSS_SELECTOR, 'a.clubs-container[href="/feuille-match?matchId=70764"]')
if link_game_1.is_enabled() and link_game_1.is_displayed:
    print("Link is clickable")
    link_game_1.click()
    time.sleep(1)
else:
    print("Link is not clickable")
    
stats_game_1 = driver.find_element(By.ID, 'nav-title-matchpage-stats')
if stats_game_1.is_enabled() and stats_game_1.is_displayed:
    print("Link is clickable")
    stats_game_1.click()
    time.sleep(10)
else:
    print("Link is not clickable")



# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.LINK_TEXT, "Calendrier/Résultats"))
#     )
#     element.click()
# except Exception as e:
#     print(e)
#     driver.quit()
