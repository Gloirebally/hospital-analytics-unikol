import pandas as pd

def charger_donnees(fichier):
    return pd.read_excel(fichier)

def nettoyer_donnees(df):
    df = df.drop_duplicates()
    df = df.dropna()
    return df
