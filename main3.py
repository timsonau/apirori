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

    currentCandidatesTable  = get_c1(data_dict)
    currentFrequencyTable = get_l1(currentCandidatesTable)

    k = 2
    while(len(currentCandidatesTable) > 0):

        currentCandidatesTable = apriori_gen(currentFrequencyTable, k)
        if(len(currentCandidatesTable) > 0):
            for transaction in data_dict.values():
                subsets = subset(set(transaction), k)
                for s in subsets:
                    if s in currentCandidatesTable:
                        currentCandidatesTable[s] += 1
            print(f"*******C{k}*********")
            print(currentCandidatesTable)
            currentFrequencyTable = get_freqeuncey_dict(currentCandidatesTable)
            print(f"*******L{k}*********")
            print(currentFrequencyTable)
            k+= 1


    
    
    print(data_dict)


def dfToDict(df):
    return df.set_index('TID')['item_IDs'].str.split(', ').to_dict()

def get_c1(data):
    c1_dict = {}

    for transaction in data.values():
        for item in transaction:
            item_set = frozenset([item])
            if  item_set in c1_dict:
                c1_dict[item_set] += 1
            else:
                c1_dict[item_set] = 1

    return c1_dict
    
def get_l1(data):
    min_sup = 2
    l1_dict = {}
    for key in data:
        if data[key] >= min_sup:
            l1_dict[key] = data[key]

    return l1_dict

def get_freqeuncey_dict(c):
    min_sup = 2
    l_dict = {}
    for key in c:
        if c[key] >= min_sup:
            l_dict[key] = c[key]
    return l_dict

def apriori_gen(L, k):
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







if __name__ == '__main__':
    main()
