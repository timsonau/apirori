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

    #df = pd.read_csv('AllElectronic.csv')
    # create the DataFrame
    df = pd.DataFrame({'TID': ['T100', 'T200', 'T300', 'T400', 'T500', 'T600', 'T700', 'T800', 'T900'],
                    'items_IDs': ['I1, I2, I5', 'I2, I4', 'I2, I3', 'I1, I2, I4', 'I1, I3', 'I2, I3', 'I1, I3', 'I1, I2, I3, I5', 'I1, I2, I3']})

    # make item_ids seperated store as a list
    df['items_IDs'] = df['items_IDs'].str.split(', ')
    # get the candidates table
    c1 = get_candidates_table(df, 1)
    print(c1)
    l1 = get_freq_n_itemset(c1, 1)
    print(l1)

    c2 = get_candidates_table(df, 2)
    print(c2)
    l2 = get_freq_n_itemset(c2, 2)
    print(l2)

    c3 = get_candidates_table(df, 3)
    print(c3)
    l3 = get_freq_n_itemset(c3, 2)
    print(l3)



def clean_data_frame(df):
    col_0 = df.columns[0]
    col_1 = df.columns[1]
    ids = df[col_1].str.split(', ')
    return pd.DataFrame({col_0: df[col_0].repeat(ids.str.len()), col_1 : ids.sum()})


#returns all posible combination of length n
def get_combinations(df, n):
    combinations_list = list(combinations(set(df['items_IDs'].explode()), n))
    return combinations_list

def get_candidates_table(df, n):
    combo_list = list(combinations(set(df['items_IDs'].explode()), n))
    item_set_occurence = {}

    #for combo in combo_list:
    for combo in combo_list:
        item_set_occurence.setdefault(combo, 0)

    for combo in combo_list:
        for row in df.itertuples():
            if set(combo).issubset(set(row[2])):
                item_set_occurence[combo] += 1
    return pd.DataFrame.from_dict(item_set_occurence, orient='index', columns=['sup_count'])

def get_freq_n_itemset(df, n):
    min_sup = 2
    l1 = df[df['sup_count'] >= min_sup]
    return l1

if __name__ == '__main__':
    main()
