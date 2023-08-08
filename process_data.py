import json


def add_full_time_results(all_games_data):
    for game_data in all_games_data:
        if game_data[5] > game_data[6]:
            game_data.insert(7, "H")
        else:
            game_data.insert(7, "NH")

def add_matchday(all_games_data):
    counter = 0
    for game_data in all_games_data:
        game_data.insert(1, (counter//10)+1)
        counter += 1


if __name__ == "__main__":
    # championship_input = input("Championship : ")
    # season_input = input("Season : ")
    # year_input = input("Year : ")
    # month_input = input("Month : ")

    # json_file_path = f"data/{championship_input}/{season_input}/{month_input}_{year_input}.json"
    json_file_path = "data/LaLiga/2022-2023/2022_2023_data.json"

    with open(json_file_path, "r") as json_file:
        games_data = json.load(json_file)

    add_full_time_results(games_data)
    add_matchday(games_data)

    print(games_data[0])

    
    