import requests
import json
import sqlite3
import pandas as pd




connection = sqlite3.connect('anime.db')
cursor = connection.cursor()

# s = requests.get('https://animechan.vercel.app/api/quotes')
responseList = []
# print(s.json())
# responseList.append(s.json())
for i in range(10):
    s = requests.get('https://animechan.vercel.app/api/quotes')
    responseList += s.json()

# print(responseList)
for i in responseList:
    print(i)
# print(responseList)

# print(responseList[1])



cursor.execute('''
          CREATE TABLE IF NOT EXISTS animeQuotes
          ([anime] TEXT, [character] TEXT, [quote] TEXT)
          ''')

for i in responseList:
    print(i['anime'])
    cursor.execute('''
          INSERT INTO animeQuotes (anime, character, quote)
                VALUES
                (?, ?, ?)
          ''', (i['anime'], i['character'], i['quote']))

cursor.execute(''' 
SELECT * FROM animeQuotes
''')


df = pd.DataFrame(cursor.fetchall())
print (df)

connection.commit()
connection.close()