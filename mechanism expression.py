import pandas as pd
import numpy as np

# In this file we will analyse the "expression" of each board game mechanism
# in a user's collection.
# First we will obtain the distribution of mechanisms in bgg from the file
# bggmechanismscount.csv, ie we will normalize the count.
# Then we will also normalize the mechanism count for each user, and then calculate
# Expression = User%/BGG%.

bggdf = pd.read_csv("bggmechanismscount.csv")
userdf = pd.read_csv("Ray&Jennie_mechanisms.csv")
name = "Ray&Jennie"
userdf.reset_index()
userdf.columns = ['mechanism', 'count']
bggdf['percent'] = (bggdf['count']*100) / bggdf['count'].sum()
userdf['percent'] = (userdf['count']*100) / userdf['count'].sum()

bggdf.set_index('mechanism', inplace=True)
userdf.set_index('mechanism', inplace=True)
userdf = pd.merge(userdf, bggdf, on='mechanism', how='inner')
userdf['expression'] = np.around(userdf['percent_x'] / userdf['percent_y'], decimals=1)
userdf['count'] = userdf['count_x']
userdf = userdf[['count', 'expression']]
print('\n')
print('Top 20 most common board game mechanisms and their expression.')
print(name)
ranked = userdf.sort_values(by='count', ascending=False).reset_index()
ranked.set_index(ranked.index.map(lambda x: x + 1), inplace=True)
print(ranked.head(20))
