"""
How does the overall equipment cost influence round outcome?
"""

import pandas as pd
from cleverminer import cleverminer

df = pd.read_csv("./data/csgo_round_snapshots_processed.csv")


# values are between 0 and 40000 - make bins of width 5k (and change beginning to be able to include 0)
df.loc[:, ['ct_overall_investment', 't_overall_investment']].describe()
investment_bins = list(range(0, 41000, 5000))
investment_bins[0] = -0.01
df['ct_overall_investment_binned'] = pd.cut(df['ct_overall_investment'], bins=investment_bins)
df['t_overall_investment_binned'] = pd.cut(df['t_overall_investment'], bins=investment_bins)

# get investment difference between ct and t buyable value
df['ct_investment_surplus'] = df['ct_overall_investment'] - df['t_overall_investment']
df['ct_investment_surplus'].describe()
# make bins from -35000 to 35000 with bins of width 5k
investment_diffs_bins = list(range(-35000, 36000, 5000))
df['ct_investment_surplus_binned'] = pd.cut(df['ct_investment_surplus'], bins=investment_diffs_bins)

# filter only columns we'll use
df = df.loc[:, ['round_winner', 'ct_overall_investment_binned', 't_overall_investment_binned',
                'ct_investment_surplus_binned']]

clm = cleverminer(df=df,
                  proc='4ftMiner',
                  quantifiers={'conf': 0.6, 'Base': 10000},
                  ante={
                      'attributes': [
                          {'name': 'ct_investment_surplus_binned', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 'ct_overall_investment_binned', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                          {'name': 't_overall_investment_binned', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                      ],
                      'minlen': 1, 'maxlen': 3, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'round_winner', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                      ],
                      'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  # cond={
                  #     'attributes': [
                  #       {'name': 'GCity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                  #       {'name': 'GSex', 'type': 'subset', 'minlen': 1, 'maxlen': 2}
                  #     ],
                  #     'minlen': 1, 'maxlen': 2, 'type': 'con'}
                  )

print(clm.result)
clm.print_summary()
# from the rules, we can see that teams with more investment on their side tend to win (rules 1 and 2)
# if teams do not have invested a lot, they lose (rules 3, 4, 7)
# if teams invest a lot (15000 and above), they tend to win (rest of rules)
"""
List of rules:
RULEID BASE  CONF  AAD    Rule
     1 14006 0.650 +0.276 ct_investment_surplus_binned((-5000, 0]) => round_winner(T) | ---
     2 10900 0.680 +0.386 ct_investment_surplus_binned((5000, 10000]) => round_winner(CT) | ---
     3 22704 0.714 +0.400 ct_overall_investment_binned((-0.01, 5000.0]) => round_winner(T) | ---
     4 11074 0.714 +0.400 ct_overall_investment_binned((5000.0, 10000.0]) => round_winner(T) | ---
     5 11745 0.649 +0.323 ct_overall_investment_binned((20000.0, 25000.0]) => round_winner(CT) | ---
     6 13639 0.663 +0.353 ct_overall_investment_binned((25000.0, 30000.0]) => round_winner(CT) | ---
     7 25441 0.721 +0.472 t_overall_investment_binned((-0.01, 5000.0]) => round_winner(CT) | ---
     8 13379 0.682 +0.337 t_overall_investment_binned((15000.0, 20000.0]) => round_winner(T) | ---
     9 15337 0.626 +0.228 t_overall_investment_binned((20000.0, 25000.0]) => round_winner(T) | ---
"""
clm.print_rulelist()
clm.print_rule(1)
