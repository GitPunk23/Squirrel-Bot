import json

data_filename = 'data.json'
data_cache = None  # Store the data in-memory

def read_data():
    global data_cache
    if data_cache is None:
        try:
            with open(data_filename, 'r') as file:
                data_cache = json.load(file)
        except FileNotFoundError:
            data_cache = {"house_chips": 10000, "players": []}
            write_data()  # Create the file if not exists
    return data_cache

def write_data():
    global data_cache
    with open(data_filename, 'w') as file:
        json.dump(data_cache, file, indent=2)

def print_all_data():
    data = read_data()
    print("House Chips:", data["house_chips"])
    print("Players:")
    for player in data["players"]:
        print(player)
    print()

def get_house_chips():
    data = read_data()
    return data["house_chips"]

def update_house_chips(new_chips):
    data = read_data()
    data["house_chips"] = new_chips
    write_data()

def get_players():
    data = read_data()
    return data["players"]

def add_player(player):
    data = read_data()
    data["players"].append(player)
    write_data()

def remove_player(discord_username):
    data = read_data()
    players = data["players"]
    
    # Find the player by Discord username
    for player in players:
        if player["discord_username"] == discord_username:
            players.remove(player)
            write_data()
            return True  # Player removed successfully
    
    return False  # Player not found
