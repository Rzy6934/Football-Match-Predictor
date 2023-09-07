import json

championships = ["Bundesliga", "LaLiga", "Ligue 1", "Premier League", "Serie A"]
seasons = ["2021-2022", "2022-2023"]
nb_week_games = 0
teams = []

all_data_dict = {}
teams_agg_goals_dict = {}
keys = ["Date", "HT", "AT", "HTHG", "ATHG", "HTFG", "ATFG", "HTPoss", "ATPoss", "HTC", "ATC", "HTTS", "ATTS", "HTSOnT", "ATSOnT", "HTSOffT", "ATSOffT", "HTSB", "ATSB", "HTTP", "ATTP", "HTPS", "ATPS", "HTKP", "ATKP", "HTDA", "ATDA", "HTDW", "ATDW", "HTDS", "ATDS", "HTAW", "ATAW", "HTAS", "ATAS", "HTDA", "ATDA", "HTOA", "ATOA", "HTTT", "ATTT", "HTTS", "ATTS", "HTTSucc", "ATTSucc", "HTI", "ATI", "HTFC", "ATFC", "HTOC", "ATOC"]
counter = 0

def transform_season_format(season):
    parts = season.split("-")
    return f"{parts[0]}_{parts[1]}"

def get_teams(all_games_data, nb_week_games):
    for game_data in all_games_data[0:nb_week_games]:
        teams.append(game_data[1])
        teams.append(game_data[2])

# def add_full_time_results(all_games_data):
#     for game_data in all_games_data:
#         if game_data[5] > game_data[6]:
#             game_data.insert(7, "H")
#         else:
#             game_data.insert(7, "NH")

# def add_matchday(all_games_data, nb_week_games):
#     counter = 0
#     for game_data in all_games_data:
#         game_data.insert(1, (counter//nb_week_games)+1)
#         counter += 1

def get_agg_goals(all_games_data):
    all_teams_agg_goals_scored = []
    all_teams_agg_goals_conceded = []
    team_agg_goals_scored = []
    team_agg_goals_conceded = []
    agg_goals_scored = 0
    agg_goals_conceded = 0

    for team in teams:
        for game_data in all_games_data[1:]:
            if team in game_data:
                team_index = game_data.index(team)
                if team_index == 1:
                    agg_goals_scored += game_data[5]
                    agg_goals_conceded += game_data[6]
                else:
                    agg_goals_scored += game_data[6]
                    agg_goals_conceded += game_data[5]
                team_agg_goals_scored.append(agg_goals_scored)
                team_agg_goals_conceded.append(agg_goals_conceded)
        team_agg_goals_scored.insert(0, 0)
        team_agg_goals_conceded.insert(0, 0)
        all_teams_agg_goals_scored.append(team_agg_goals_scored)
        all_teams_agg_goals_conceded.append(team_agg_goals_conceded)
        team_agg_goals_scored = []
        team_agg_goals_conceded = []
        agg_goals_scored = 0
        agg_goals_conceded = 0

    return all_teams_agg_goals_scored, all_teams_agg_goals_conceded

def generate_team_stats_dict(teams, all_teams_agg_goals_scored, all_teams_agg_goals_conceded):
    team_stats_dict = {}

    for i, team in enumerate(teams):
        team_stats_dict[team] = {
            "scored": all_teams_agg_goals_scored[i],
            "conceded": all_teams_agg_goals_conceded[i]
        }

    return team_stats_dict


if __name__ == "__main__":
    while True:
        championship_input = input("Championship : ")
        if championship_input in championships:
            break
        else:
            print("Invalid championship. Please enter a valid championship.")

    while True:
        season_input = input("Season : ")
        if season_input in seasons:
            break
        else:
            print("Invalid season. Please enter a valid season.")

    season_formatted = transform_season_format(season_input)

    json_data_path = f"data/{championship_input}/{season_input}/{season_formatted}_data.json"

    with open(json_data_path, "r") as json_file:
        all_games_data = json.load(json_file)

    # add_full_time_results(all_games_data)

    if championship_input == "Bundesliga":
        nb_week_games = 9
    else:
        nb_week_games = 10

    # print(nb_week_games)

    # add_matchday(all_games_data, nb_week_games)

    get_teams(all_games_data, nb_week_games)

    all_teams_agg_goals_scored, all_teams_agg_goals_conceded = get_agg_goals(all_games_data)

    print(teams)

    for i, data in enumerate(all_games_data, start=1):
        data_dict = dict(zip(keys, data))
        
        # Initialisez les clés "HTAGS", "ATAGS", "HTAGC", "ATAGC" à None
        data_dict["HTAGS"] = None
        data_dict["ATAGS"] = None
        data_dict["HTAGC"] = None
        data_dict["ATAGC"] = None
        
        # Ajoutez le sous-dictionnaire au dictionnaire principal avec une clé numérique
        all_data_dict[str(i)] = data_dict

    teams_agg_goals_dict = generate_team_stats_dict(teams, all_teams_agg_goals_scored, all_teams_agg_goals_conceded)

# print(all_data_dict)
print(teams_agg_goals_dict)