import pandas as pd

def charger_donnees(fichier):
    return pd.read_excel(fichier)

def nettoyer_donnees(df):
    df = df.drop_duplicates()
    df = df.dropna()
    return df
def detecter_anomalies(df):
    """Détecte les anomalies simples dans les données"""
    anomalies = []
    if 'age' in df.columns:
        outliers = df[(df['age'] < 0) | (df['age'] > 120)]
        if len(outliers) > 0:
            anomalies.append(f"{len(outliers)} patients avec âge anormal")
    return anomalies if anomalies else ["Aucune anomalie majeure détectée"]

def generer_rapport(df):
    """Génère un rapport texte basique"""
    rapport = f"Rapport d'analyse\n"
    rapport += f"Nombre de patients : {len(df)}\n"
    rapport += f"Colonnes analysées : {', '.join(df.columns)}\n"
    return rapport

def detecter_anomalies_avancees(df):
    """Détection d'anomalies avancée - version simplifiée"""
    return detecter_anomalies(df)
