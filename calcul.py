import sys
import sqlite3
import elo
import file
import ast
import re
import display_score

def elo_tournament(tournament, elo_system, player):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sets WHERE tournament_key = ?", (tournament,))
    rows = c.fetchall()
    for row in rows:
        if (row[6] != -1 and row[7] != -1):
            score = recognize_winner(row[4], row[5], row[3])
            create_profil(player, str(row[4]), str(row[5]))
            battle(elo_system, str(row[4]), str(row[5]), score, player)
    conn.close()

def recognize_winner(ID1, ID2, winner):
    if winner == ID1:
        return 1
    elif winner == ID2:
        return 2
    else:
        return 0

def create_profil(player, player1, player2):
    if player1 not in player:
        gamer1 = elo.Player(player1, 1200, 0)
        player[player1] = gamer1.rating, gamer1.set
    if player2 not in player:
        gamer2 = elo.Player(player2, 1200, 0)
        player[player2] = gamer2.rating, gamer2.set

def battle(elo_system, player1, player2, score, player):
    player1 = elo.Player(player1, player[player1][0], player[player1][1])
    player2 = elo.Player(player2, player[player2][0], player[player2][1])
    elo_system.update_rating(player1, player2, score)
    player[player1.name] = player1.rating, player1.set
    player[player2.name] = player2.rating, player2.set

def add_informations(player):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    for key in player:
        c.execute("SELECT * FROM players WHERE player_id = ?", (key,))
        rows = c.fetchall()
        for row in rows:
            player[key] = player[key], row[2], row[9], row[13]
    conn.close()

def sort_by_elo(player, x):
    if x == 0:
        return sorted(player.items(), key=lambda x: x[1][0][0], reverse=True)
    else:
        return sorted(player, key=lambda x: x[1][0][0], reverse=True)

def print_player(player):
    count = 1
    for x in range(len(player)):
        print(count, "{:.0f}".format(player[x][1][0][0]), player[x][1][1], player[x][1][2], player[x][1][3])
        count += 1

def fusion_character(*tuples):
    liste_commune = {}
    for tpl in tuples:
        for key, value in ast.literal_eval(tpl).items():
            if key in liste_commune:
                liste_commune[key] += value
            else:
                liste_commune[key] = value
    return liste_commune

def check_same_name(player):
    to_remove = []
    for x in range(len(player)):
        for y in range(x + 1, len(player)):
            if player[x][1][1] == player[y][1][1]:
                new_set = player[x][1][0][1] + player[y][1][0][1]
                new_elo = ((player[x][1][0][0] + player[y][1][0][0]) / 2)
                if player[x][1][3] == '""' or player[y][1][3] == '""':
                    if player[x][1][3] == '""':
                        new_character = player[y][1][3]
                    elif player[y][1][3] == '""':
                        new_character = player[x][1][3]
                    else:
                        new_character = fusion_character(player[0][1][3], player[0][1][3])
                else:
                    new_character = fusion_character(player[x][1][3], player[y][1][3])
                player[x] = (player[x][0], ((new_elo, new_set), player[x][1][1], player[x][1][2], new_character))
                to_remove.append(y)
    for index in sorted(to_remove, reverse=True):
        del player[index]
    return player

def modifier_tuple(data):
    if isinstance(data, str):
        data = ast.literal_eval(data)
    modified_dict = {}
    try:
        for key, value in data.items():
            modified_key = key.split("/")[-1]
            modified_dict[modified_key] = value
    except AttributeError:
        modified_dict["mario"] = 1
    return modified_dict

def filter_data(data):
    result = []
    for item in data:
        highest_usage = max(item.values())
        filtered_item = {character: usage for character, usage in item.items() if usage >= 0.3 * highest_usage}
        result.append(filtered_item)    
    return result

def modify_data(char, data):
    data_list = [list(item) for item in data]
    for x, element in enumerate(char):
        inner_list = list(data_list[x][1])
        inner_list[3] = element
        data_list[x][1] = tuple(inner_list)
    return tuple(data_list)

def clean_data(data):
    cleaned_data = []
    for item in data:
        cleaned_item = ""
        for key, value in item.items():
            cleaned_key = re.sub(r'[{}0-9:,\'\"]', '', key)
            cleaned_value = re.sub(r'[{}0-9:,\'\"]', '', str(value))
            cleaned_item += cleaned_key + " " + cleaned_value
        cleaned_data.append(cleaned_item.strip())
    return cleaned_data

def split_character_data(data):
    split_data = []
    for item in data:
        item = list(item)
        character_info = list(item[1])
        character_info[3] = character_info[3].split(" ")
        item[1] = tuple(character_info)
        item = tuple(item)
        split_data.append(item)
    return tuple(split_data)

def tournament(list, elo_system):
    player = {}
    for x in range(len(list)):
        elo_tournament(list[x], elo_system, player)
    add_informations(player)
    player = sort_by_elo(player, 0)
    player = check_same_name(player)
    player = sort_by_elo(player, 1)
    x = 0
    char = []
    while x < len(player):
        char.append(modifier_tuple(player[x][1][3]))
        x += 1
    char = filter_data(char)
    char = clean_data(char)
    char = modify_data(char, player)
    #print_player(char)
    char = split_character_data(char)
    display_score.game(char)

def main():
    new_file = file.find_file_txt() ## find the file txt
    name_tournament = file.read_file(new_file) ## read the file txt and return a list of tournament name
    elo_system = elo.EloSystem() ## create the elo system
    tournament_list = file.convert_name_key_tournaments(name_tournament)
    tournament(tournament_list, elo_system) ## calculate the elo of each player in the tournament

if __name__ == "__main__":
    sys.exit(main())