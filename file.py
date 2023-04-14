import os
import sqlite3

def find_file_txt():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".txt"):
                return file

def read_file(file):
    contenu = []
    try:
        with open(file, 'r') as fichier:
            contenu = [ligne.strip() for ligne in fichier.readlines()]
    except FileNotFoundError:
        print("Le fichier n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    return contenu

def convert_name_key_tournament(name, list):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tournament_info WHERE cleaned_name = ?", (name,))
    rows = c.fetchall()
    for row in rows:
        list.append(row[1])
    conn.close()
    return list
