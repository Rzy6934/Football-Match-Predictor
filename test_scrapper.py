import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class Scrapper:
    def __init__(self, championship, season):
        self.championship = championship
        self.season = season
        self.all_games_data = []