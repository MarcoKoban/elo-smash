import sys
import sqlite3
import elo

def number_tournament(ID):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tournament_info")
    rows = c.fetchall()
    count = 0
    for x in range(len(rows)):
        if ID in rows[x][15]:
            count += 1
    print(count)
    conn.close()
    return count

def print_tournament(ID):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tournament_info")
    rows = c.fetchall()
    for x in range(len(rows)):
        if ID in rows[x][15]:
            print(rows[x][2])
    conn.close()

def nbr_set(ID):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sets WHERE (p1_id = ? OR p2_id = ?) AND p1_score != -1 AND p2_score != -1", (ID, ID))
    count = c.fetchone()[0]
    conn.close()
    return count

def nbr_win(ID):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sets WHERE winner_id = ? AND p1_score != -1 AND p2_score != -1", (ID,))
    count = c.fetchone()[0]
    conn.close()
    return count

def nbr_loss(set, win):
    return set - win

def pourcent_win(set, win):
    if set == 0:
        return 0
    else:
        pourcentage = (win / set) * 100
        return round(pourcentage, 2)

def elo_tournament(tournament, elo_system, joueurs):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sets WHERE tournament_key = ?", (tournament,))
    rows = c.fetchall()
    for row in rows:
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

def main():
    elo_system = elo.EloSystem()
    joueurs = {}
    elo_tournament("king-of-the-hive__l-hexagone-1", elo_system, joueurs)
    print(joueurs)

if __name__ == "__main__":
    sys.exit(main())
