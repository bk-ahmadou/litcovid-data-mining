from apyori import apriori
import pandas as pd
import os.path

def database_transaction_matrix(references):
    # Crée une matrice binaire pour les données de référence
    # Les clés sont les identifiants des références et les valeurs sont les éléments associés à chaque référence
    keys = list(references.keys())
    values = list(set([val for sublist in references.values() for val in sublist]))
    df = pd.DataFrame(0, index=keys, columns=values)
    for k, vals in references.items():
        for v in vals:
            df.at[k, v] = 1
    return df

def apriori_frequent_itemsets(input_file, output_file, support_threshold):
    # Analyse des règles d'association à partir des données textuelles
    if not os.path.isfile(input_file):
        print("Le fichier d'entrée n'existe pas.")
        return
    
    references = {}
    with open(input_file, 'r') as input_txt:
        # Itère sur chaque ligne du document pour extraire les références
        for line in input_txt:
            ref = line.strip().split("/")
            pmid = ref[0]
            ref = ref[1:]
            references[pmid] = ref
            
    data = database_transaction_matrix(references)
    data.to_csv('input_data.csv', index=False)

    # Analyse des règles d'association à partir de la matrice binaire
    frequent_itemsets = pd.DataFrame(list(apriori(data.astype('bool'), min_support=support_threshold, use_colnames=True)))
    
    if len(frequent_itemsets) == 0:
        print("Aucun ensemble fréquent trouvé.")
        return
    
    frequent_itemsets.to_csv(output_file, index=False)

# Exemple d'utilisation
apriori_frequent_itemsets("./pmid-refs-exist.txt", "./result1.txt", 0.5)
