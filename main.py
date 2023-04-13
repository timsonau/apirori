# -----------------------------------------#
# Apirori Algoithm Main Function Stubbed
#
#
#
# -----------------------------------------#

import pandas as pd
from itertools import combinations

def main():
    # read csv file

    df = pd.read_csv('AllElectronic.csv')
    
    df = df.rename(columns={df.columns[0]: 'TID', df.columns[1]: 'item_IDs'})
    # make item_ids seperated store as a list
    df['item_IDs'] = df['item_IDs'].str.split(', ')
    total_item_set = set(df['item_IDs'].explode())
    print(total_item_set)
    for n in range(1, 4):
        print(f"******C{n} Candidates Table******")
        candidates = get_candidates_table(df, n)
        print(candidates)
        frequent_itemsets = get_freq_n_itemset(candidates, n)
        print(f"******L{n} after pruning******")
        print(frequent_itemsets)
        print(f"******Association rules derived from L{n}******")
        #print_associtation_rules(frequent_itemsets)



def clean_data_frame(df):
    col_0 = df.columns[0]
    col_1 = df.columns[1]
    ids = df[col_1].str.split(', ')
    return pd.DataFrame({col_0: df[col_0].repeat(ids.str.len()), col_1 : ids.sum()})


#returns all posible combination of length n
def get_combinations(df, n):
    combinations_list = list(combinations(set(df['item_IDs'].explode()), n))
    return combinations_list

def get_candidates_table(df, n):
    combo_list = list(combinations(set(df['item_IDs'].explode()), n))
    combo_occurence = {}

    #for combo in combo_list:
    for combo in combo_list:
        combo_occurence.setdefault(combo, 0)

    for combo in combo_list:
        for row in df.itertuples():
            if set(combo).issubset(set(row[2])):
                combo_occurence[combo] += 1
    return pd.DataFrame.from_dict(combo_occurence, orient='index', columns=['sup_count'])

def get_freq_n_itemset(df, n):
    min_sup = 2
    l1 = df[df['sup_count'] >= min_sup]
    return l1


if __name__ == '__main__':
    main()
