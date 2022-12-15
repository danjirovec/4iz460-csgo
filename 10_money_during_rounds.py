import matplotlib.pyplot as plt
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

logger.info("Starting graph generation. Reading data...")
# get processed data
df = pd.read_csv("data/csgo_round_snapshots_processed.csv")

logger.info("Creating data for graph")
# get average money for rounds
money = df.groupby('round_number', as_index=False)['ct_money'].mean()
money = money.merge(df.groupby('round_number', as_index=False)['t_money'].mean(), on='round_number')
money = money.rename(columns={'ct_money': 'ct_average', 't_money': 't_average'})

# get first quartile of money for rounds
money = money.merge(df.groupby('round_number', as_index=False)['ct_money'].quantile(q=0.25), on='round_number')
money = money.merge(df.groupby('round_number', as_index=False)['t_money'].quantile(q=0.25), on='round_number')
money = money.rename(columns={'ct_money': 'ct_1qt', 't_money': 't_1qt'})

# get third quartile of money for rounds
money = money.merge(df.groupby('round_number', as_index=False)['ct_money'].quantile(q=0.75), on='round_number')
money = money.merge(df.groupby('round_number', as_index=False)['t_money'].quantile(q=0.75), on='round_number')
money = money.rename(columns={'ct_money': 'ct_3qt', 't_money': 't_3qt'})

logger.info("Generating graph and saving")
fig = plt.subplots(figsize=(12, 8))
# plot lines denoting important match rounds (31st beginning with extra money and 16th end of match (potentially))
plt.axvline(x=16, color='#3c3226', alpha=0.1)
plt.axvline(x=31, color='#3c3226', alpha=0.1)
# plot IQR
plt.fill_between(money['round_number'], money['ct_1qt'], money['ct_3qt'], alpha=0.2, color='#5d79ae', label='CT IQR')
plt.fill_between(money['round_number'], money['t_1qt'], money['t_3qt'], alpha=0.2, color='#de9b35', label='T IQR')
# plot averages
plt.plot(money['round_number'], money['ct_average'], color='#5d79ae', label='CT')
plt.plot(money['round_number'], money['t_average'], color='#de9b35', label='T')

# add title and labels, legend
plt.suptitle("Team money across round numbers", fontsize=15)
plt.title("Average money amount and its interquartile range (IQR)", fontsize=8)
plt.xlabel('Round')
plt.ylabel('Money available ($)')
plt.legend()

plt.savefig('./outputs/money_by_round.png')
logger.info("Done")
