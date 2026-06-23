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
def generer_top5_insights(df, stats, analyse):
    insights = []
    if 'service_top' in analyse:
        insights.append({'icone': '🏥', 'titre': 'Service le plus fréquenté', 'valeur': analyse['service_top'], 'desc': f"{analyse['service_top_count']} patients", 'couleur': '#1976D2'})
    if 'diag_top' in analyse:
        insights.append({'icone': '🩺', 'titre': 'Diagnostic principal', 'valeur': analyse['diag_top'], 'desc': 'Cas le plus récurrent', 'couleur': '#42A5F5'})
    insights.append({'icone': '👥', 'titre': 'Total patients', 'valeur': stats['total_patients'], 'desc': 'Sur la période', 'couleur': '#0A1F44'})
    insights.append({'icone': '🎂', 'titre': 'Âge moyen', 'valeur': f"{stats['age_moyen']} ans", 'desc': 'Population', 'couleur': '#64B5F6'})
    if stats['temps_attente_moyen'] > 0:
        insights.append({'icone': '⏱', 'titre': 'Temps attente moyen', 'valeur': f"{stats['temps_attente_moyen']} min", 'desc': 'À optimiser', 'couleur': '#90CAF9'})
    return insights[:5]

def calculer_score_hospitalier(stats, df):
    score = 50
    if stats['temps_attente_moyen'] < 15: score += 20
    elif stats['temps_attente_moyen'] < 30: score += 10
    if stats['total_patients'] > 20: score += 10
    if stats['nb_services'] > 3: score += 10
    return min(100, score)
