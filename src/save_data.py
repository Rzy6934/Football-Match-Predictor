from pymongo import MongoClient
import json

client = MongoClient("mongodb://127.0.0.1:27017/mongosh?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.1", 27017)

db = client["football"]

main_folders = ["Bundesliga", "LaLiga", "Ligue 1", "Premier League", "Serie A"]

def transform_season_format(season):
    parts = season.split("-")
    return f"{parts[0]}_{parts[1]}"

for main_folder in main_folders:
    main_collection = db[main_folder]
    season_folders = ["2021-2022", "2022-2023"]
    
    for season_folder in season_folders:
        formatted_season = transform_season_format(season_folder)
        with open(f"data/{main_folder}/{season_folder}/{formatted_season}_final_data.json", "r") as json_file:
            game_data = json.load(json_file)
            
        season_doc = {
            "season" : season_folder,
            "game_data" : game_data
        }
        
        main_collection.insert_one(season_doc)
        
client.close()