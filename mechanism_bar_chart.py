# This script plots a horizontal bar chart with
# a user's percentage of game mechanisms compared
# to the percentage in the bgg database.
#
# It requires both  the "Name_mechanisms.csv" file obtained
# from running the "mechanisms_user.py" script, and, for greater
# precision, a recent "bggmechanismscount.csv" file obtained
# from running the "mechanisms_bgg.py" script.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    # In order to use this script on your own files, you must alter:
    # 1. The user's name to be featured on the plot.
    user_name = "Example"
    # 2. The path to the csv file with the user's collection data:
    file = "GFLima_mechanisms.csv"

    bgg_dataframe = pd.read_csv("bggmechanismscount.csv")
    user_dataframe = pd.read_csv(file)
    ranked_dataframe = data_clean_and_prep(user_dataframe=user_dataframe, bgg_dataframe=bgg_dataframe)
    make_plot(dataframe=ranked_dataframe, name=user_name)
    return None


def data_clean_and_prep(user_dataframe, bgg_dataframe):
    userdf = user_dataframe.copy()
    bggdf = bgg_dataframe.copy()
    userdf.reset_index()
    userdf.columns = ['mechanism', 'count']
    bggdf['percent'] = (bggdf['count']*100) / bggdf['count'].sum()
    userdf['percent'] = (userdf['count']*100) / userdf['count'].sum()
    bggdf.set_index('mechanism', inplace=True)
    userdf.set_index('mechanism', inplace=True)
    userdf = pd.merge(userdf, bggdf, on='mechanism', how='inner')
    ranked = userdf.sort_values(by='count_x', ascending=False).reset_index()
    return ranked


def make_plot(dataframe, name):
    plt.figure(figsize=(8, 12), dpi=80)
    blue = np.array((82/255, 255/255, 229/255))/1.1
    green = np.array((95/255, 214/255, 77/255))/1.1
    orange = np.array((255/255, 162/255, 57/255))/1.1
    red = np.array((255./255, 97./255, 48./255))/1.1
    Y = dataframe['mechanism'][:20][::-1]
    X1 = dataframe['percent_x'][:20][::-1]
    X2 = dataframe['percent_y'][:20][::-1]
    # bars for users
    plt.barh(Y, X1, height=0.35, align='edge', alpha=1.0, color=blue, label=name)
    # bars for bgg
    plt.barh(Y, X2, height=-0.35, align='edge', alpha=0.70, color=red, label='bgg')
    plt.title('Percentage of top 20 board game mechanisms\ncompared to boardgamegeek.com.')
    plt.xlabel('Percentage')
    vals = range(1, int(np.ceil(max(X2.max(), X1.max()))))
    plt.xticks(vals, labels=[str(x) + '%' for x in vals])
    plt.legend(loc='center right', fontsize='large')
    plt.grid(visible=True, axis='x', linestyle='--')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()

