# Based on 'publication_date_histogram.py'.
# This script plots a *stacked* histogram of the publication date
# for the games in a user's collection with colors for each weight
# class. It expects the csv file obtained when one downloads collection
# data from boardgamegeek.com. For an explanation on how to obtain
# this, see https://boardgamegeek.com/wiki/page/Data_Mining

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def data_clean(dataframe):
    # select relevant columns and drop duplicates
    df = dataframe[['objectname', 'baverage', 'avgweight', 'yearpublished', 'itemtype']].drop_duplicates()
    # remove expansions
    df = df[df['itemtype'] == 'standalone']
    # removing old games (before 1900)
    df = df[df['yearpublished'] >= 1900]
    # add weight class column
    df['weightclass'] = df['avgweight'].map(np.floor)
    # name the classes since this is what will show up on plot
    weightnames = dict(zip([0.0, 1.0, 2.0, 3.0, 4.0],
                           ['light', 'light - medium', 'medium', 'medium - heavy', 'heavy']
                           ))
    df['weightclass'] = df['weightclass'].map(weightnames)
    return df


def group_by_weight(dataframe):
    # grouping by weightclass
    data_grouped = dataframe['yearpublished'].groupby(dataframe['weightclass'])
    weightgroups, data_frames = zip(*data_grouped)
    return weightgroups, data_frames


def get_colors(weightlist:list) -> list:
    # manual choice of colors
    my_blue = np.array((82 / 255, 255 / 255, 229 / 255)) / 1.1
    my_green = np.array((95 / 255, 214 / 255, 77 / 255)) / 1.1
    my_yellow = np.array((255/255, 231/255, 74/255)) / 1.1
    my_orange = np.array((255 / 255, 162 / 255, 57 / 255)) / 1.1
    my_red = np.array((255. / 255, 97. / 255, 48. / 255)) / 1.1
    my_colors = [my_blue, my_green, my_yellow, my_orange, my_red]
    colorofweights = dict(zip(['light', 'light - medium', 'medium', 'medium - heavy', 'heavy'],
                              my_colors))
    colors = [colorofweights[weight] for weight in weightlist]
    return colors


def get_year_range(dataframe):
    years = dataframe['yearpublished']
    end = years.max()
    start = years.min()
    return start, end


def make_plot(data_frames, weightgroups, colors_used, year_start, year_end, name):
    # create matplotlib figure
    plt.figure(figsize=(20, 8), dpi=80)
    plt.hist(data_frames, bins=range(year_start, year_end+2), align='mid', width=0.8, stacked=True, color=colors_used, alpha=1.0)
    pos = np.arange(year_start, year_end+2) + 0.4
    yearslabels = np.arange(year_start, year_end+2)
    plt.xticks(pos, yearslabels, rotation=90, alpha=0.8)
    plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True)
    plt.grid(visible=True, axis='y', linestyle='--')
    plt.suptitle(name, fontsize='x-large', ha='center', weight='bold')
    plt.title('Games by Publication Date and Weight, 1900 - 2022', ha='center')
    plt.legend(labels=weightgroups, loc='upper left')
    plt.show()
    pass


def main():
    # In order to use this script on your own files, you must alter:
    # 1. The user's name to be featured on the plot.
    name = "Test"
    # 2. The path to the csv file with the user's collection data:
    file = "Data files/Weber_bgg_data.csv"

    bgg_data = pd.read_csv(file)
    bgg_data = data_clean(bgg_data)
    weightgroups, data_frames = group_by_weight(bgg_data)
    colors_used = get_colors(weightgroups)
    year_start, year_end = get_year_range(bgg_data)
    make_plot(data_frames=data_frames,
              weightgroups=weightgroups,
              colors_used=colors_used,
              year_start=year_start,
              year_end=year_end,
              name=name)
    pass


if __name__ == '__main__':
    main()


