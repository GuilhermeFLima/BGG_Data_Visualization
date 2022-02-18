# Based on 'publication_date_histogram.py'.
# This script plots a *stacked* histogram of the publication date
# for the games in a user's collection with colors for each weight
# class. It expects the csv file obtained when one downloads collection
# data from boardgamegeek.com. For an explanation on how to obtain
# this, see https://boardgamegeek.com/wiki/page/Data_Mining


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# In order to use this script on your own files, you must alter the
# following two variables:
#
# 1. The user's name to be featured on the plot.
name = "Test"
# 2. The path to the csv file with the user's collection data:
file = "test_bgg_data.csv"

# read csv file into pandas DataFrame
bgg_data = pd.read_csv(file)


def data_clean(dataframe):
    # select relevant columns and drop duplicates
    df = dataframe[['objectname', 'baverage', 'avgweight', 'yearpublished', 'itemtype']].drop_duplicates()
    # remove expansions
    df = df[df['itemtype'] == 'standalone']
    # removing old games (before 1900)
    df = df[df['yearpublished'] >= 1900]
    # add weight class column
    df['weightclass'] = df['avgweight'].map(np.floor)
    return df


bgg_data = data_clean(bgg_data)

# grouping by weightclass
data_grouped = bgg_data['yearpublished'].groupby(bgg_data['weightclass'])
# extracting just the dataframes from groupby object
data_frames = [df.astype('object') for group, df in data_grouped]
weightgroups = [group for group, df in data_grouped]

weightnames = dict(zip([0.0, 1.0, 2.0, 3.0, 4.0],
                       ['light', 'light - medium', 'medium', 'medium - heavy', 'heavy']
                       ))

weightgroupsnamed = [weightnames[group] for group in weightgroups]

# pandas Series for publication years
years = bgg_data['yearpublished']

# create matplotlib figure
plt.figure(figsize=(20, 8), dpi=80)

data_max = years.max()
data_min = years.min()

# manual choice of colors
mycolors = np.array([(82/255, 255/255, 229/255),
                       (95/255, 214/255, 77/255),
                       (255/255, 231/255, 74/255),
                       (255/255, 162/255, 57/255),
                       (255./255, 97./255, 48./255)])
# divide to add hue
mycolors = mycolors/(1.1, 1.1, 1.1)
colorofweights = dict(zip(['light', 'light - medium', 'medium', 'medium - heavy', 'heavy'],
                          mycolors))
colors = [colorofweights[groupname] for groupname in weightgroupsnamed]
# Series histogram
plt.hist(data_frames, bins=range(data_min, data_max+2), align='mid', width=0.8, stacked=True, color=colors, alpha=1.0)
pos = np.arange(data_min, data_max+2) + 0.4
yearslabels = np.arange(data_min, data_max+2)
plt.xticks(pos, yearslabels, rotation=90, alpha=0.8)
plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True)
plt.grid(visible=True, axis='y', linestyle='--')
plt.suptitle(name, fontsize='x-large', ha='center', weight='bold')
plt.title('Games by Publication Date and Weight, 1900 - 2022', ha='center')
plt.legend(labels=weightgroupsnamed, loc='upper left')
plt.show()



