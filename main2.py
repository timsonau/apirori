import pandas as pd
from itertools import combinations
import ast
import itertools
def main():
    # read csv file

    df = pd.read_csv('AllElectronic.csv')
    
    df = df.rename(columns={df.columns[0]: 'TID', df.columns[1]: 'item_IDs'})
    # make item_ids seperated store as a list
    df['item_IDs'] = df['item_IDs'].str.split(', ')
    total_item_set = set(df['item_IDs'].explode())

    #create the candidates table c1
    k=1
    c1 = find_candidate_kth_itemset(df, df, k)
    l1 = find_freq_1_itemSet(c1)
    print(l1)
    k+=1
    c2 = find_candidate_kth_itemset(l1, df, k)
    print(c2)
    l2 = find_freq_1_itemSet(c2)
    print(l2)
    k+=1
    x = find_item_set_combination_test(l2,3)
    c3 = find_candidate_kth_itemset(l2, df, k)
    print(c3)


def find_candidate_1_itemset(df):
    item_set = set(df['item_IDs'].explode())
    c1_dict = {}
    for i, row in df.iterrows():
        for item in item_set:
            if set(item.split(', ')) <= set(row['item_IDs'] ):
                if str(item) in c1_dict:
                    c1_dict[str(item)] += 1
                else:
                    c1_dict[str(item)] = 1
    
    c1_dict = [{'Item Set': x, 'Sup Count': y} for x, y in c1_dict.items()]
    c1 = pd.DataFrame(c1_dict)
    return c1

def find_item_set_combination(df, n):
    item_set = set(df["Item Set"])
    combinations = list(itertools.combinations(item_set, n))
    combinations = {', '.join(pair) for pair in combinations}
    return combinations


def find_item_set_combination_test(df, n):
    item_set = set(df["Item Set"])
    return set([i.union(j) for i in item_set for j in item_set if len(i.union(j)) == n])
def find_freq_1_itemSet(candidates_table):
    min_sup_count = 2
    return candidates_table[candidates_table['Sup Count'] >= min_sup_count]


# find the kth candidate itemset
# freq_table: data frame representing the k-th frequent itemset
# original_data: data frame of the csv containg the original data
# isFirst: boolean indicating if this is the first candiadate table
def find_candidate_kth_itemset(freq_table, original_data, k):
    item_set = set(original_data['item_IDs'].explode()) if k==1 else find_item_set_combination(freq_table, k) 
    c1_dict = {key: 0 for key in item_set}
    for i, row in original_data.iterrows():
        for item in item_set:
            if set(item.split(', ')) <= set(row['item_IDs']):
                if str(item) in c1_dict:
                    c1_dict[str(item)] += 1
                else:
                    c1_dict[str(item)] = 1

    c1_dict = [{'Item Set': x, 'Sup Count': y} for x, y in c1_dict.items()]
    c1 = pd.DataFrame(c1_dict)
    return c1




if __name__ == '__main__':
    main()
