import json


def add_full_time_results(all_games_data):
    for game_data in all_games_data:
        if game_data[5] > game_data[6]:
            game_data.insert(7, "H")
        else:
            game_data.insert(7, "NH")

def add_matchday(all_games_data, counter_starting_value):
    counter = counter_starting_value
    for game_data in all_games_data:
        game_data.insert(1, (counter//10)+1)
        counter += 1


if __name__ == "__main__":
    championship_input = input("Championship : ")
    season_input = input("Season : ")
    year_input = input("Year : ")
    month_input = input("Month : ")

    json_file_path = f"data/{championship_input}/{season_input}/{month_input}_{year_input}.json"

    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    print(type(json_data))
    print(json_data)