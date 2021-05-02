# %%
import pandas as pd
import pymongo

client = pymongo.MongoClient("mongo")
db_pr = client['exercices']
collection_pr = db_pr['player_review']

# %%

def load_data():
    file = open('data.txt', 'r', encoding='utf-8')
    players = []
    data = file.read().splitlines()
    for line in data:
        left = line.split('|')[0]
        right = line.split('|')[1]
        if left == 'Player':
            player = {
                'name': right,
                'games': {}
            }
            players.append(player)
        else:
            player['games'][left] = float(right)
    return players

players = load_data()


# %%
collection_pr.insert_one(players[0])
# %%
