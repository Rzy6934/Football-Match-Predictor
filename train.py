import json

championships = ["Bundesliga", "LaLiga", "Ligue 1", "Premier League", "Serie A"]
seasons = ["2021-2022", "2022-2023"]
columns = ["Date", "Matchweek", "HomeTeam", "AwayTeam", "Hpossession", "Apossession", "HcornersTotal", "AcornersTotal", "HshotsTotal", "AshotsTotal", "HshotsOnTarget", "AshotsOnTarget", "HshotsOffTarget", "AshotsOffTarget", "HshotsBlocked", "AshotsBlocked", "HpassesTotal", "ApassesTotal", "HpassSuccess", "ApassSuccess", "HpassesKey", "ApassesKey", "HdribblesAttempted", "AdribblesAttempted", "HdribblesWon", "AdribblesWon", "HdribbleSuccess", "AdribbleSuccess", "HaerialsWon", "AaerialsWon", "HaerialSuccess", "AaerialSuccess", "HdefensiveAerials", "AdefensiveAerials", "HoffensiveAerials", "AoffensiveAerials", "HtacklesTotal", "AtacklesTotal", "HtackleSuccessful", "AtackleSuccessful", "HtackleSuccess", "AtackleSuccess", "Hinterceptions", "Ainterceptions", "HfoulsCommited", "AfoulsCommited", "HoffsidesCaught", "AoffsidesCaught", "HaggregateGoalsScored", "AaggregateGoalsScored", "HaggregateGoalsConceded", "AaggregateGoalsConceded", "HaggregatePoints", "AaggregatePoints", "HgoalsDifference", "AgoalsDifference", "HlastFiveGamesStreak", "AlastFiveGamesStreak", "HfiveWinsStreaks", "AfiveWinsStreaks", "HfiveLossesStreaks", "AfiveLossesStreaks", "HthreeWinsStreaks", "AthreeWinsStreaks", "HthreeLossesStreaks", "AthreeLossesStreaks"] 

def transform_season_format(season):
    parts = season.split("-")
    
    return f"{parts[0]}_{parts[1]}"

def get_all_data(championships, seasons):
    all_games_data = []
    
    for championship in championships:
        for season in seasons:
            formatted_season = transform_season_format(season)
            with open(f"data/{championship}/{season}/{formatted_season}_final_data.json", "r") as json_file:
                game_data = json.load(json_file)
                all_games_data += game_data
                game_data = []
                
    return all_games_data

# def dataframe_converter(all_games_data):
    
    

if __name__ == "__main__":
    all_games_data = get_all_data(championships, seasons)
    print(len(all_games_data))
    print(all_games_data[3650:3651+1])