import sys
import sqlite3
import elo
import file
import ast

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

def sort_by_elo(player):
    return sorted(player.items(), key=lambda x: x[1][0][0], reverse=True)

def print_player(player):
    count = 1
    for x in range(len(player)):
        print(count, "{:.0f}".format(player[x][1][0][0]), player[x][1][1], player[x][1][2])
        count += 1

def fusion_character(*tuples):
    liste_commune = {}
    for tpl in tuples:
        for key, value in ast.literal_eval(tpl).items():
            if key in liste_commune:
                liste_commune[key] += value
            else:
                liste_commune[key] = value
    print(liste_commune)
    return liste_commune

def check_same_name(player):
    to_remove = []
    for x in range(len(player)):
        for y in range(x + 1, len(player)):
            if player[x][1][1] == player[y][1][1]:
                new_set = player[x][1][0][1] + player[y][1][0][1]
                new_elo = ((player[x][1][0][0] + player[y][1][0][0]) / 2)
                new_character = fusion_character(player[x][1][3], player[y][1][3])
                player[x] = (player[x][0], ((new_elo, new_set), player[x][1][1], player[x][1][2], new_character))
                to_remove.append(y)
    for index in sorted(to_remove, reverse=True):
        del player[index]
    return player

def modify_tuple(player):
    x = 1
    for i in player:
        if not i[1][3]:
            print("no character", x)
        else:
            print(x, i[1][3])
        x += 1

def tournament(list, elo_system):
    player = {}
    for x in range(len(list)):
        elo_tournament(list[x], elo_system, player)
    add_informations(player)
    player = sort_by_elo(player)
    player = check_same_name(player)
    print_player(player)

def main():
    new_file = file.find_file_txt() ## find the file txt
    elo_system = elo.EloSystem() ## create the elo system
    name_tournament = file.read_file(new_file) ## read the file txt and return a list of tournament name
    list = []
    for x in range(len(name_tournament)): ## convert the tournament name to the tournament key
        list = file.convert_name_key_tournament(name_tournament[x], list)
    tournament(list, elo_system) ## calculate the elo of each player in the tournament

if __name__ == "__main__":
    sys.exit(main())