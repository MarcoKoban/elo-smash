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

def convert_name_key_tournament(name, list):
    conn = sqlite3.connect('ultimate_player_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tournament_info WHERE cleaned_name = ?", (name,))
    rows = c.fetchall()
    for row in rows:
        list.append(row[1])
    conn.close()
    return list
