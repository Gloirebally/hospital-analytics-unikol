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
def analyse_avancee(df):
    """Analyse avancée pour générer insights"""
    analyse = {}

    if 'Service' in df.columns:
        analyse['service_top'] = df['Service'].value_counts().index[0]
        analyse['service_top_count'] = df['Service'].value_counts().iloc[0]

    if 'Diagnostic' in df.columns:
        analyse['diag_top'] = df['Diagnostic'].value_counts().index[0]

    if 'Temps_attente' in df.columns:
        analyse['attente_max'] = df['Temps_attente'].max()

    if 'Age' in df.columns:
        analyse['age_min'] = df['Age'].min()
        analyse['age_max'] = df['Age'].max()

    return analyse
