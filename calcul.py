import sys
import sqlite3
import elo
import file
import os

def elo_tournament(tournament, elo_system, joueurs):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sets WHERE tournament_key = ?", (tournament,))
    rows = c.fetchall()
    for row in rows:
        if (row[6] != -1 and row[7] != -1):
            score = recognize_winner(row[4], row[5], row[3])
            create_profil(joueurs, str(row[4]), str(row[5]))
            battle(elo_system, str(row[4]), str(row[5]), score, joueurs)
    conn.close()

def recognize_winner(ID1, ID2, winner):
    if winner == ID1:
        return 1
    elif winner == ID2:
        return 2
    else:
        return 0

def create_profil(joueurs, player1, player2):
    if player1 not in joueurs:
        joueur1 = elo.Player(player1, 1200, 0)
        joueurs[player1] = joueur1.rating, joueur1.set
    if player2 not in joueurs:
        joueur2 = elo.Player(player2, 1200, 0)
        joueurs[player2] = joueur2.rating, joueur2.set

def battle(elo_system, player1, player2, score, joueurs):
    player1 = elo.Player(player1, joueurs[player1][0], joueurs[player1][1])
    player2 = elo.Player(player2, joueurs[player2][0], joueurs[player2][1])
    elo_system.update_rating(player1, player2, score)
    joueurs[player1.name] = player1.rating, player1.set
    joueurs[player2.name] = player2.rating, player2.set

def add_pseudo(joueurs):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    for key in joueurs:
        c.execute("SELECT * FROM players WHERE player_id = ?", (key,))
        rows = c.fetchall()
        for row in rows:
            joueurs[key] = joueurs[key], row[2]
    conn.close()

def sort_by_elo(joueurs):
    return sorted(joueurs.items(), key=lambda x: x[1][0][0], reverse=True)

def print_player(joueurs):
    count = 1
    for x in range(len(joueurs)):
        print(count, "{:.0f}".format(joueurs[x][1][0][0]), joueurs[x][1][1])
        count += 1

def tournament(list, elo_system):
    joueurs = {}
    for x in range(len(list)):
        elo_tournament(list[x], elo_system, joueurs)
    add_pseudo(joueurs)
    joueurs = sort_by_elo(joueurs)
    print_player(joueurs)

def main():
    new_file = file.find_file_txt() ## trouve le premier fichier txt
    elo_system = elo.EloSystem() ## initialise le système d'élo
    name_tournament = file.read_file(new_file) ## lit le fichier txt et le stock dans une liste
    list = []
    for x in range(len(name_tournament)): ## converti le nom du tournoi en clé du tournoi
        list = file.convert_name_key_tournament(name_tournament[x], list)
    tournament(list, elo_system) ## lance le calcul d'elo


if __name__ == "__main__":
    sys.exit(main())
