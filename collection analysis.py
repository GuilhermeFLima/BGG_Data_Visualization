import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

name = 'Kara'
file = 'howlsthunder_bgg_data.csv'
# read csv file into pandas DataFrame
bgg_data = pd.read_csv(file)

# select relevant columns and drop duplicates
bgg_data = bgg_data[['objectname', 'baverage', 'avgweight', 'yearpublished', 'itemtype']].drop_duplicates()

# remove expansions
bgg_data_sa = bgg_data[bgg_data['itemtype'] == 'standalone']
# removing old games (before 1900)
bgg_data_sa_recent = bgg_data_sa[bgg_data_sa['yearpublished'] >= 1900]
print(bgg_data_sa_recent.describe())
# pandas Series for publication years
bgg_data_sa_recent_yp = bgg_data_sa_recent['yearpublished']

# create matplotlib figure
plt.figure(figsize=(20, 8), dpi=80)

data_max = bgg_data_sa_recent_yp.max()
data_min = bgg_data_sa_recent_yp.min()

# Series histogram
h = plt.hist(bgg_data_sa_recent_yp, bins=range(data_min, data_max+2), align='mid', width=0.8)
pos = np.arange(data_min, data_max+2) + 0.4
yearslabels = np.arange(data_min, data_max+2)
plt.xticks(pos, yearslabels, rotation=90, alpha=0.8)
plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True)
plt.grid(visible=True, axis='y', linestyle='--')
plt.suptitle(name, fontsize='x-large', ha='center', weight='bold')
plt.title('Games by Publication Date, 1900 - 2022', ha='center')
plt.show()



