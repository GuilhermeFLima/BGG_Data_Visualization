# This script plots a histogram of the publication date
# for the games in a user's collection. It expects the csv
# file obtained when one downloads collection data from
# boardgamegeek.com. For an explanation on how to obtain
# this, see https://boardgamegeek.com/wiki/page/Data_Mining

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    # In order to use this script on your own files, you must alter:
    # 1. The user's name to be featured on the plot.
    name = "Test"
    # 2. The path to the csv file with the user's collection data:
    file = "test_bgg_data.csv"

    # read csv file into pandas DataFrame
    bgg_data = pd.read_csv(file)
    series = data_clean(dataframe=bgg_data)
    year_start, year_end = get_year_range(series=series)
    make_plot(series=series,
              year_start=year_start,
              year_end=year_end,
              name=name)
    pass


def data_clean(dataframe):
    # select relevant columns and drop duplicates
    df = dataframe[['objectname', 'baverage', 'avgweight', 'yearpublished', 'itemtype']].drop_duplicates()
    # remove expansions
    df = df[df['itemtype'] == 'standalone']
    # removing old games (before 1900)
    df = df[df['yearpublished'] >= 1900]
    # pandas Series for publication years
    series = df['yearpublished']
    return series


def get_year_range(series):
    end = series.max()
    start = series.min()
    return start, end


def make_plot(series, year_start, year_end, name):
    # create matplotlib figure
    plt.figure(figsize=(20, 8), dpi=80)
    plt.hist(series, bins=range(year_start, year_end+2), align='mid', width=0.8)
    pos = np.arange(year_start, year_end+2) + 0.4
    yearslabels = np.arange(year_start, year_end+2)
    plt.xticks(pos, yearslabels, rotation=90, alpha=0.8)
    plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True)
    plt.grid(visible=True, axis='y', linestyle='--')
    plt.suptitle(name, fontsize='x-large', ha='center', weight='bold')
    plt.title('Games by Publication Date, 1900 - 2022', ha='center')
    plt.show()
    pass


if __name__ == '__main__':
    main()

