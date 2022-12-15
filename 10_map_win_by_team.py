import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MaxAbsScaler

# TODO delete
import os
os.chdir(r"F:/School/Magistr/3. semestr/Pokročilé přístupy k dobývání znalostí z databází 4IZ460/semestralni_prace/4iz460-csgo")

# get processed data
df = pd.read_csv("data/csgo_round_snapshots_processed.csv")

# group by wins
df_grouped = df.groupby(by=[df['map'], df['round_winner']], as_index=False)['time_left'].count()
df_grouped = df_grouped.rename(columns={'time_left': 'wins'})
df_grouped_rel = df_grouped.copy(deep=True)

# get relative wins
for g_map in df_grouped['map'].unique():
    df_grouped_rel.loc[df_grouped_rel['map'] == g_map, 'wins'] = df_grouped_rel.loc[df_grouped_rel['map'] == g_map, 'wins']/max(df_grouped_rel.loc[df_grouped['map'] == g_map, 'wins'])


# set width of each bar
bar_width = 0.33
# initialize a figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('Team wins by map', fontsize=25)
plt.subplots_adjust(bottom=0.2)

# fig = plt.figure(figsize=(12, 8))

# get heights of bar: height = amount of wins
ct_wins = df_grouped.loc[df_grouped['round_winner'] == 'CT', 'wins'].tolist()
t_wins = df_grouped.loc[df_grouped['round_winner'] == 'T', 'wins'].tolist()
ct_wins_rel = df_grouped_rel.loc[df_grouped_rel['round_winner'] == 'CT', 'wins'].tolist()
t_wins_rel = df_grouped_rel.loc[df_grouped_rel['round_winner'] == 'T', 'wins'].tolist()

# get positioning of teams on plot x-axis
x_ct = [x+bar_width/2 for x in range(len(ct_wins))]
x_t = [x + bar_width for x in x_ct]

# plot bars - absolute count
ax1.bar(x_ct, ct_wins, color='#5d79ae', width=bar_width, label='CT')
ax1.bar(x_t, t_wins, color='#de9b35', width=bar_width, label='T')
# Add labels
ax1.set_title('Absolute count')
ax1.set_xlabel('Map')
ax1.set_ylabel('Rounds won')
ax1.set_xticks([x + bar_width for x in range(len(ct_wins))], df_grouped.loc[df_grouped['round_winner'] == 'CT', 'map'].tolist(), rotation=45)
ax1.tick_params(axis='x', which='major', length=0)
ax1.legend()

# plot bars - relative count
ax2.bar(x_ct, ct_wins_rel, color='#5d79ae', width=bar_width, label='CT')
ax2.bar(x_t, t_wins_rel, color='#de9b35', width=bar_width, label='T')
# Add labels
ax2.set_title('Relative count')
ax2.set_xlabel('Map')
ax2.set_ylabel('Rounds won (%)')
ax2.set_xticks([x + bar_width for x in range(len(ct_wins))], df_grouped_rel.loc[df_grouped_rel['round_winner'] == 'CT', 'map'].tolist(), rotation=45)
ax2.tick_params(axis='x', which='major', length=0)
ax2.legend()

fig.savefig('./outputs/wins_by_map.png')