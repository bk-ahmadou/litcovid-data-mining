from apyori import apriori
import pandas as pd

def create_binary_matrix(references):
    keys = list(references.keys())
    values = list(set([val for sublist in references.values() for val in sublist]))
    df = pd.DataFrame(0, index=keys, columns=values)
    for k, vals in references.items():
        for v in vals:
            df.at[k, v] = 1
    return df


# def create_binary_matrix(references):
#     keys = list(references.keys())
#     values = set([val for sublist in references.values() for val in sublist])
#     df = pd.DataFrame(0, index=keys, columns=values)
#     for k, vals in references.items():
#         for v in vals:
#             df.at[k, v] = 1
#     return df


def apriori_frequent_itemsets(input_file, output_file, support_threshold):
    references = {}

    with open(input_file, 'r') as input_txt:
        # Itere sur chaque ligne du document
        for line in input_txt:
            # On essaye de split("/")
            ref = line.split("/")
            pmid = ref[0]
            ref = ref[1:]
            
            references[pmid] = ref
    #print(create_binary_matrix(references))
    data = create_binary_matrix(references)
    data.to_csv('input_data.csv', index=False)

    print(data)
    frequent_itemsets = pd.DataFrame(list(apriori(data.astype('bool'), min_support=support_threshold, use_colnames=True)))
    print(frequent_itemsets["support"])
    frequent_itemsets.to_csv(output_file, index=False)


apriori_frequent_itemsets("./pmid-refs-exist.txt","./result.txt",0.9)