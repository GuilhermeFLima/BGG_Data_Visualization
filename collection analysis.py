import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

name = 'GFLima'
file = 'GFLima_bgg_data.csv'
# read csv file into pandas DataFrame
bgg_data = pd.read_csv(file)

# select relevant columns and drop duplicates
bgg_data = bgg_data[['objectname', 'baverage', 'avgweight', 'rank', 'yearpublished', 'itemtype']].drop_duplicates()

# remove expansions
bgg_data_sa = bgg_data[bgg_data['itemtype'] == 'standalone']
# pandas Series for publication years
bgg_data_sa_yp = bgg_data_sa['yearpublished']
# removing old games (before 1900)
bgg_data_sa_yp_recent = bgg_data_sa_yp[bgg_data_sa['yearpublished'] >= 1900]
data_max = bgg_data_sa_yp_recent.max()
data_min = bgg_data_sa_yp_recent.min()
print(bgg_data_sa_yp_recent.describe())

# create matplotlib figure
plt.figure(figsize=(20, 8), dpi=80)
# Series histogram
bgg_data_sa_yp_recent.plot.hist(bins=range(data_min, data_max+2), align='mid', width=0.8)
pos = np.arange(data_min, data_max+2) + 0.4
yearslabels = np.arange(data_min, data_max+2)
plt.xticks(pos, yearslabels, rotation=90, alpha=0.8)
plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True)
plt.grid(visible=True, axis='y', linestyle='--')
plt.suptitle(name, fontsize='x-large', ha='center', weight='bold')
plt.title('Games by Publication Date, 1900 - 2022', ha='center')
plt.show()