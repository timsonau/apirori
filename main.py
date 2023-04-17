import pandas as pd
from itertools import combinations
import ast
import itertools
def main():
    # read csv file

    df = pd.read_csv('AllElectronic.csv')
    
    df = df.rename(columns={df.columns[0]: 'TID', df.columns[1]: 'item_IDs'})
    # make item_ids seperated store as a list
    data_dict = dfToDict(df)

    min_sup_count = int(input("Enter Minimium Support Count: "))
    
    currentCandidatesTable  = get_c1(data_dict)
    print("*************************C1*************************")
    display_as_table(currentCandidatesTable)

    currentFrequencyTable = get_frequency_dict(currentCandidatesTable, min_sup_count)
    print("*************************L1*************************")
    display_as_table(currentFrequencyTable)
    k = 2
    while(len(currentFrequencyTable) > 0):
        currentCandidatesTable = apriori_gen(currentFrequencyTable, k)
        if (len(currentCandidatesTable) == 0): break
        
        for transaction in data_dict.values():
            subsets = subset(set(transaction), k)
            for s in subsets:
                if s in currentCandidatesTable:
                    currentCandidatesTable[s] += 1
        print(f"*************************C{k}*************************")
        display_as_table(currentCandidatesTable)
        currentFrequencyTable = get_frequency_dict(currentCandidatesTable, min_sup_count)
        if(len(currentFrequencyTable) > 0):
            print(f"*************************L{k}*************************")
            display_as_table(currentFrequencyTable)
        else:
            print(f"Frequency table L{k} empty, end execution")
        k+= 1
    
    #where to derive association rules from currentFrquecyTable
    display_as_table(currentFrequencyTable)
def dfToDict(df):
    """
    dfToDict: converts a pandas data frame object into a dictionary

    :param df: pandas data frame
    :return: dictionary containing data frame values
    """ 
    return df.set_index('TID')['item_IDs'].str.split(', ').to_dict()

def get_c1(data):
    """
    get_c1: gets the intial candidates table

    :param data: dictionary with the transaction data
    :return: dictionary containing frozen item set as keys and support count as values
    """ 
    c1_dict = {}

    for transaction in data.values():
        for item in transaction:
            item_set = frozenset([item])
            if  item_set in c1_dict:
                c1_dict[item_set] += 1
            else:
                c1_dict[item_set] = 1

    return c1_dict
    
def get_frequency_dict(C, min_sup):
    """
    get_frequency_dict: gets the intial candidates table

    :param C, the ck candidates table
    :min_sup, minimum support count threshold
    :return: dictionary containing frequnet item sets
    """ 
    l_dict = {}
    for key in C:
        if C[key] >= min_sup:
            l_dict[key] = C[key]
    return l_dict

def apriori_gen(L, k):
    """
    get_frequency_dict: gets the intial candidates table

    :param L, the Lk-1 frequent item set
    :min_sup, minimum support count threshold
    :return: dictionary containing frequnet item sets
    """ 
    candidates_dict = {}
    for l1 in L.keys():
        for l2 in L.keys():
            item_set_1 = set(l1)
            item_set_2 = set(l2)
            in_common = item_set_1.intersection(item_set_2)
            if(len(in_common )== k-2):
                candidate_item_set = item_set_1.union(item_set_2)
                if(not(frozenset(candidate_item_set) in candidates_dict)):
                    if(not(has_infrequent_subset(candidate_item_set, L, k))):
                        candidates_dict[frozenset(candidate_item_set)] = 0
                    
    return candidates_dict      

def has_infrequent_subset(canidate, L, k):
    pset = subset(canidate, k-1)
    for set in pset:
        if(not(set in L)):
            return True
    return False

def subset(set, k):
    p = []
    for subset in itertools.combinations(set, k):
        p.append(frozenset(subset))
    return p

def display_as_table(dict):
    df = pd.DataFrame(list(dict.items()), columns=['Item Set', 'Support Count'])
    print(df)

if __name__ == '__main__':
    main()
