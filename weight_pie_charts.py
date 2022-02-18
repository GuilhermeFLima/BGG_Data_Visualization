# This script plots pie chart of the weight classes
# for the games in a user's collection. It expects the csv
# file obtained when one downloads collection data from
# boardgamegeek.com. For an explanation on how to obtain
# this, see https://boardgamegeek.com/wiki/page/Data_Mining

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    # In order to use this script on your own files, you must alter:
    # 1. The user's name to be featured on the plot.
    name = "Test"
    # 2. The path to the csv file with the user's collection data:
    file = "test_bgg_data.csv"
    # read csv file into pandas DataFrame
    bgg_data = pd.read_csv(file)
    bgg_data = data_clean(bgg_data)
    data_grouped = group_by_weight(bgg_data)
    data_grouped = percent_column(data_grouped)
    data_grouped = color_column(data_grouped)
    make_plot(data_grouped, name=name)
    return None


def data_clean(dataframe):
    # select relevant columns and drop duplicates
    df = dataframe[['objectname', 'baverage', 'avgweight', 'yearpublished', 'itemtype']].drop_duplicates()
    # remove expansions
    df = df[df['itemtype'] == 'standalone']
    # removing old games (before 1900)
    df = df[df['yearpublished'] >= 1900]
    # add weight class column
    df['weightclass'] = df['avgweight'].map(np.floor)
    weightnames = dict(zip([0.0, 1.0, 2.0, 3.0, 4.0],
                           ['light', 'light - medium', 'medium', 'medium - heavy', 'heavy']
                           ))
    df['weightclass'] = df['weightclass'].map(weightnames)
    return df


def group_by_weight(dataframe):
    # grouping by weightclass
    data_grouped = dataframe['weightclass'].groupby(dataframe['weightclass'])
    series = data_grouped.count()
    df = pd.DataFrame(series)
    df['count'] = df['weightclass']
    df.drop(['weightclass'], axis=1, inplace=True)
    df.reset_index(inplace=True)
    return df


def percent_column(dataframe):
    df = dataframe.copy()
    df['percent'] = (100*df['count'])/df['count'].sum()
    return df


def color_column(dataframe):
    my_blue = np.array((82 / 255, 255 / 255, 229 / 255)) / 1.1
    my_green = np.array((95 / 255, 214 / 255, 77 / 255)) / 1.1
    my_yellow = np.array((255 / 255, 231 / 255, 74 / 255)) / 1.1
    my_orange = np.array((255 / 255, 162 / 255, 57 / 255)) / 1.1
    my_red = np.array((255. / 255, 97. / 255, 48. / 255)) / 1.1
    my_colors = [my_blue, my_green, my_yellow, my_orange, my_red]
    colorofweights = dict(zip(['light', 'light - medium', 'medium', 'medium - heavy', 'heavy'],
                              my_colors))
    df = dataframe.copy()
    df['color'] = df['weightclass'].map(colorofweights)
    return df


def make_plot(dataframe, name):
    plt.figure(figsize=(9, 9), dpi=80)
    plt.pie(dataframe['percent'], autopct='%1.1f%%', shadow=True, colors=dataframe['color'])
    plt.legend(labels=dataframe['weightclass'], loc='upper right')
    plt.suptitle(name, fontsize='x-large', ha='center', weight='bold')
    plt.title('Breakdown of Games by Weight\n 1900 - 2022', ha='center')
    plt.show()
    return None


if __name__ == '__main__':
    main()

