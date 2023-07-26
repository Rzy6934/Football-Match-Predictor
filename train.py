import pandas as pd

ligue_1_2022_2023_data = pd.read_json("data/Ligue 1/2022_2023_data.json")

columns = ["Date", "Matchweek", "HomeTeam", "AwayTeam", "FHHTG", "FHATG", "FTHTG", "FTATG", "FTR", "HTS", "ATS", "HTST", "ATST", "HTP", "ATP", "HTPP", "ATPP"]

ligue_1_2022_2023_data.columns = columns

print(ligue_1_2022_2023_data)
