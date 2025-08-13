import sqlite3
import json

with open("base_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

connection = sqlite3.connect("bar_base_.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS drinks (
        barcode INTEGER,
        drink_name TEXT,
        bottle_weight INTEGER,
        density REAL,
        type TEXT             
               )
""")

for barcode, drinks in data.items():
    for drink in drinks:
        cursor.execute('''
            INSERT OR REPLACE INTO drinks (barcode, drink_name, bottle_weight, density, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (barcode, drink["drink_name"], drink["bottle_weight"], drink['difference'], drink["type"]))


connection.commit()
connection.close()