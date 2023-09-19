import json

championships = ["Bundesliga", "LaLiga", "Ligue 1", "Premier League", "Serie A"]
seasons = ["2021-2022", "2022-2023"]
nb_week_games = 0
teams = []
counter = 0

def transform_season_format(season):
    parts = season.split("-")
    return f"{parts[0]}_{parts[1]}"

def get_teams(all_games_data, nb_week_games):
    for game_data in all_games_data[0:nb_week_games]:
        teams.append(game_data[1])
        teams.append(game_data[2])

def add_default_stats(all_games_data):
    zeros_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for game_data in all_games_data:
        game_data += zeros_list

    return all_games_data

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

def get_agg_points(all_games_data):
    all_teams_agg_points = []
    all_teams_wins_losses = []
    team_agg_points = []
    team_wins_losses = []
    agg_points = 0

    for team in teams:
        for game_data in all_games_data[1:]:
            if team in game_data[1]:
                if game_data[5] > game_data[6]:
                    agg_points += 3
                    team_wins_losses.append("W")
                elif game_data[5] == game_data[6]:
                    agg_points += 1
                    team_wins_losses.append("D")
                else:
                    agg_points += 0
                    team_wins_losses.append("L")

                team_agg_points.append(agg_points)

            elif team in game_data[2]:
                if game_data[6] > game_data[5]:
                    agg_points += 3
                    team_wins_losses.append("W")
                elif game_data[6] == game_data[5]:
                    agg_points += 1
                    team_wins_losses.append("D")
                else:
                    agg_points += 0
                    team_wins_losses.append("L")

                team_agg_points.append(agg_points)
        team_agg_points.insert(0, 0)
        all_teams_agg_points.append(team_agg_points)
        team_agg_points = []
        agg_points = 0

    return all_teams_agg_points

def get_win_losses(all_games_data):
    all_teams_wins_losses = []
    team_wins_losses = []

    for team in teams:
        for game_data in all_games_data:
            if team in game_data[1]:
                if game_data[5] > game_data[6]:
                    team_wins_losses.append("W")
                elif game_data[5] == game_data[6]:
                    team_wins_losses.append("D")
                else:
                    team_wins_losses.append("L")

            elif team in game_data[2]:
                if game_data[6] > game_data[5]:
                    team_wins_losses.append("W")
                elif game_data[6] == game_data[5]:
                    team_wins_losses.append("D")
                else:
                    team_wins_losses.append("L")

        all_teams_wins_losses.append(team_wins_losses)
        team_wins_losses = []

    return all_teams_wins_losses

def get_5g_streaks(all_teams_wins_losses):
    all_teams_5g_streaks = []
    team_5g_streaks = []
    
    for team_wins_losses in all_teams_wins_losses:
        for i in range(len(team_wins_losses)):
            if i < 5:
                streak = ["-"] * (5 - i) + team_wins_losses[:i]
            else:
                streak = team_wins_losses[i-5:i]
            team_5g_streaks.append(streak)

        concatenated_streaks = [''.join(sublist) for sublist in team_5g_streaks]

        all_teams_5g_streaks.append(concatenated_streaks)
        team_5g_streaks = []
        concatenated_streaks = []

    return all_teams_5g_streaks

def get_5_wins_losses_streaks(all_teams_5g_streaks):
    all_teams_5_wins_streaks = []
    all_teams_5_losses_streaks = []
    team_5_wins_streaks = []
    team_5_losses_streaks = []
    five_wins_streaks = 0
    five_losses_streaks = 0
    
    for team_5g_streaks in all_teams_5g_streaks:
        for streak in team_5g_streaks:
            if streak == "WWWWW":
                five_wins_streaks += 1
            elif streak == "LLLLL":
                five_losses_streaks += 1
            team_5_wins_streaks.append(five_wins_streaks)
            team_5_losses_streaks.append(five_losses_streaks)
        
        all_teams_5_wins_streaks.append(team_5_wins_streaks)
        all_teams_5_losses_streaks.append(team_5_losses_streaks)
        team_5_wins_streaks = []
        team_5_losses_streaks = []
        five_wins_streaks = 0
        five_losses_streaks = 0
        
    return all_teams_5_wins_streaks, all_teams_5_losses_streaks

def get_3_wins_losses_streaks(all_teams_5g_streaks):
    all_teams_3_wins_streaks = []
    all_teams_3_losses_streaks = []
    team_3_wins_streaks = []
    team_3_losses_streaks = []
    three_wins_streaks = 0
    three_losses_streaks = 0
    
    for team_5g_streaks in all_teams_5g_streaks:
        for streak in team_5g_streaks:
            if streak[-3:] == "WWW":
                three_wins_streaks += 1
            elif streak[-3:] == "LLL":
                three_losses_streaks += 1
            team_3_wins_streaks.append(three_wins_streaks)
            team_3_losses_streaks.append(three_losses_streaks)
        
        all_teams_3_wins_streaks.append(team_3_wins_streaks)
        all_teams_3_losses_streaks.append(team_3_losses_streaks)
        team_3_wins_streaks = []
        team_3_losses_streaks = []
        three_wins_streaks = 0
        three_losses_streaks = 0
        
    return all_teams_3_wins_streaks, all_teams_3_losses_streaks
            
def add_agg_stats(all_games_data, all_teams_agg_goals_scored, all_teams_agg_goals_conceded, all_teams_agg_points, all_teams_5g_streaks, all_teams_5_wins_streaks, all_teams_5_losses_streaks, all_teams_3_wins_streaks, all_teams_3_losses_streaks, teams):
    counter = 0
    for team, agg_goals_scored, agg_goals_conceded, agg_points, team_5g_streaks, team_5_wins_streaks, team_5_losses_streaks, team_3_wins_streaks, team_3_losses_streaks in zip(teams, all_teams_agg_goals_scored, all_teams_agg_goals_conceded, all_teams_agg_points, all_teams_5g_streaks, all_teams_5_wins_streaks, all_teams_5_losses_streaks, all_teams_3_wins_streaks, all_teams_3_losses_streaks):
        for game_data in all_games_data:
            if team in game_data[1]:
                game_data[51] = agg_goals_scored[counter]
                game_data[53] = agg_goals_conceded[counter]
                game_data[55] = agg_points[counter]
                game_data[57] = agg_goals_scored[counter] - agg_goals_conceded[counter]
                game_data[59] = team_5g_streaks[counter]
                game_data[61] = team_5_wins_streaks[counter]
                game_data[63] = team_5_losses_streaks[counter]
                game_data[65] = team_3_wins_streaks[counter]
                game_data[67] = team_3_losses_streaks[counter]
                counter += 1
            elif team in game_data[2]:
                game_data[52] = agg_goals_scored[counter]
                game_data[54] = agg_goals_conceded[counter]
                game_data[56] = agg_points[counter]
                game_data[58] = agg_goals_scored[counter] - agg_goals_conceded[counter]
                game_data[60] = team_5g_streaks[counter]
                game_data[62] = team_5_wins_streaks[counter]
                game_data[64] = team_5_losses_streaks[counter]
                game_data[66] = team_3_wins_streaks[counter]
                game_data[68] = team_3_losses_streaks[counter]
                counter += 1
        counter = 0

    return all_games_data

def add_full_time_results(all_games_data):
    for game_data in all_games_data:
        if game_data[5] > game_data[6]:
            game_data.insert(7, "H")
        else:
            game_data.insert(7, "NH")

def add_matchday(all_games_data, nb_week_games):
    counter = 0
    for game_data in all_games_data:
        game_data.insert(1, (counter//nb_week_games)+1)
        counter += 1


if __name__ == "__main__":
    # while True:
    #     championship_input = input("Championship : ")
    #     if championship_input in championships:
    #         break
    #     else:
    #         print("Invalid championship. Please enter a valid championship.")

    # while True:
    #     season_input = input("Season : ")
    #     if season_input in seasons:
    #         break
    #     else:
    #         print("Invalid season. Please enter a valid season.")

    # season_formatted = transform_season_format(season_input)
    
    championship_input = "Serie A"
    season_input = "2022-2023"
    season_formatted = transform_season_format(season_input)

    json_data_path = f"data/{championship_input}/{season_input}/{season_formatted}_data.json"

    with open(json_data_path, "r") as json_file:
        all_games_data = json.load(json_file)

    if championship_input == "Bundesliga":
        nb_week_games = 9
    else:
        nb_week_games = 10

    get_teams(all_games_data, nb_week_games)
        
    all_teams_wins_losses = get_win_losses(all_games_data)

    all_teams_5g_streaks = get_5g_streaks(all_teams_wins_losses)
    
    all_teams_5_wins_streaks, all_teams_5_losses_streaks = get_5_wins_losses_streaks(all_teams_5g_streaks)
    
    all_teams_3_wins_streaks, all_teams_3_losses_streaks = get_3_wins_losses_streaks(all_teams_5g_streaks)
    
    all_teams_agg_goals_scored, all_teams_agg_goals_conceded = get_agg_goals(all_games_data)
    
    all_teams_agg_points = get_agg_points(all_games_data)

    all_games_data_updated = add_default_stats(all_games_data)

    all_games_data_updated_final = add_agg_stats(all_games_data_updated, all_teams_agg_goals_scored, all_teams_agg_goals_conceded, all_teams_agg_points, all_teams_5g_streaks, all_teams_5_wins_streaks, all_teams_5_losses_streaks, all_teams_3_wins_streaks, all_teams_3_losses_streaks, teams)

    add_full_time_results(all_games_data_updated_final)
    
    add_matchday(all_games_data_updated_final, nb_week_games)
    
    print(all_games_data_updated_final)