# This script plots pie chart of the weight classes
# for the games in a user's collection. It expects the csv
# file obtained when one downloads collection data from
# boardgamegeek.com. For an explanation on how to obtain
# this, see https://boardgamegeek.com/wiki/page/Data_Mining

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

name = 'Test'
file = 'test_bgg_data.csv'

# read csv file into pandas DataFrame
bgg_data = pd.read_csv(file)

# select relevant columns and drop duplicates
bgg_data = bgg_data[['objectname', 'baverage', 'avgweight', 'yearpublished', 'itemtype']].drop_duplicates()

# remove expansions
bgg_data_sa = bgg_data[bgg_data['itemtype'] == 'standalone']
# removing old games (before 1900)
bgg_data_sa_recent = bgg_data_sa[bgg_data_sa['yearpublished'] >= 1900]

# add weight class column
bgg_data_sa_recent['weightclass'] = bgg_data_sa_recent['avgweight'].map(np.floor)
# grouping by weightclass
data_grouped = bgg_data_sa_recent['weightclass'].groupby(bgg_data_sa_recent['weightclass'])
weightseries = data_grouped.count()
weightdf = pd.DataFrame(weightseries)
weightdf['count'] = weightdf['weightclass']
weightdf.drop(['weightclass'], axis=1, inplace=True)
weightdf.reset_index(inplace=True)
weightnames = dict(zip([0.0, 1.0, 2.0, 3.0, 4.0],
                       ['light', 'light - medium', 'medium', 'medium - heavy', 'heavy']
                       ))

weightdf['weightclass'] = weightdf['weightclass'].map(weightnames)
weightdf['percent'] = (100*weightdf['count'])/weightdf['count'].sum()
# weightdf = weightdf[['count', 'percent']]
bggcolors2 = np.array([(82/255, 255/255, 229/255),
                       (95/255, 214/255, 77/255),
                       (255/255, 231/255, 74/255),
                       (255/255, 162/255, 57/255),
                       (255./255, 97./255, 48./255)])
# divide to add hue
bggcolors2 = bggcolors2/(1.1, 1.1, 1.1)
colorofweights = dict(zip(['light', 'light - medium', 'medium', 'medium - heavy', 'heavy'],
                          bggcolors2))
weightdf['color'] = weightdf['weightclass'].map(colorofweights)
plt.figure(figsize=(9, 9), dpi=80)
plt.pie(weightdf['percent'], autopct='%1.1f%%', shadow=True, colors=weightdf['color'])
plt.legend(labels=weightdf['weightclass'], loc='upper right')
plt.suptitle(name, fontsize='x-large', ha='center', weight='bold')
plt.title('Breakdown of Games by Weight\n 1900 - 2022', ha='center')
plt.show()