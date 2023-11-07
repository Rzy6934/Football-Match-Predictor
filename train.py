import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

championships = ["Bundesliga", "LaLiga", "Ligue 1", "Premier League", "Serie A"]
seasons = ["2021-2022", "2022-2023"]
columns = ["Date", "Matchweek", "HomeTeam", "AwayTeam", "HhalfTimeGoals", "AhalfTimeGoals", "HfullTimeGoals", "AfullTimeGoals", "FullTimeResult", 
           "Hpossession", "Apossession", "HcornersTotal", "AcornersTotal", "HshotsTotal", "AshotsTotal", "HshotsOnTarget", "AshotsOnTarget", 
           "HshotsOffTarget", "AshotsOffTarget", "HshotsBlocked", "AshotsBlocked", "HpassesTotal", "ApassesTotal", "HpassSuccess", "ApassSuccess", 
           "HpassesKey", "ApassesKey", "HdribblesAttempted", "AdribblesAttempted", "HdribblesWon", "AdribblesWon", "HdribbleSuccess", "AdribbleSuccess", 
           "HaerialsWon", "AaerialsWon", "HaerialSuccess", "AaerialSuccess", "HdefensiveAerials", "AdefensiveAerials", "HoffensiveAerials", "AoffensiveAerials", 
           "HtacklesTotal", "AtacklesTotal", "HtackleSuccessful", "AtackleSuccessful", "HtackleSuccess", "AtackleSuccess", "Hinterceptions", "Ainterceptions", 
           "HfoulsCommited", "AfoulsCommited", "HoffsidesCaught", "AoffsidesCaught", "HaggregateGoalsScored", "AaggregateGoalsScored", "HaggregateGoalsConceded", 
           "AaggregateGoalsConceded", "HaggregatePoints", "AaggregatePoints", "HgoalsDifference", "AgoalsDifference", "HlastFiveGamesStreak", "AlastFiveGamesStreak", 
           "HfiveWinsStreaks", "AfiveWinsStreaks", "HfiveLossesStreaks", "AfiveLossesStreaks", "HthreeWinsStreaks", "AthreeWinsStreaks", "HthreeLossesStreaks", "AthreeLossesStreaks"] 

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
    

def dataframe_converter(dataset, columns):
    all_games_df = pd.DataFrame(data=dataset, columns=columns)
    return all_games_df


def correlation_matrix(dataset):
    dataset_2 = dataset.copy().drop(columns=["Date", "Matchweek", "HomeTeam", "AwayTeam", "FullTimeResult", "HlastFiveGamesStreak", "AlastFiveGamesStreak"])
    plt.figure()
    sns.heatmap(dataset_2.corr(), annot= True)
    plt.show()
    

def compute_win_rate(dataset):
  n_games = dataset.shape[0]
  n_features = dataset.shape[1] - 1

  n_home_wins = len(dataset[dataset.FullTimeResult == 'H'])

  win_rate = (float(n_home_wins) / (n_games)) * 100

  print("Total number of matches: {}".format(n_games))
  print ("Number of features: {}".format(n_features))
  print( "Number of matches won by home team: {}".format(n_home_wins))
  print ("Win rate of home team: {:.2f}%".format(win_rate))

    

if __name__ == "__main__":
    all_games_data = get_all_data(championships, seasons)
    all_games_df = dataframe_converter(all_games_data, columns)
    print(all_games_df.head())
    correlation_matrix(all_games_df)
    compute_win_rate(all_games_df)
    # print(len(all_games_data[0]))
    # print(len(columns))
    # print(all_games_data[0])
    # print(all_games_data[3650:3651+1])