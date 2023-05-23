import os
import sqlite3

def find_file_txt():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".txt"):
                return file

def read_file(file):
    content = []
    try:
        with open(file, 'r', encoding='utf-8') as file:
            content = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return content

def convert_name_key_tournaments(names):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    query = "SELECT * FROM tournament_info WHERE cleaned_name = ?"

    tournament_list = []

    for name in names:
        c.execute(query, (name,))
        rows = c.fetchall()
        if len(rows) == 0:
            print("The tournament {} is not in the database.".format(name))
        else:
            for row in rows:
                tournament_list.append(row[1])

    conn.close()

    return tournament_list

