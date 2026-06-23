import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def get_theme_colors():
    """Version robuste pour détecter Light/Dark"""
    try:
        # Streamlit >= 1.28
        theme = st.get_option("theme.base")
    except:
        # Fallback si ça bug
        theme = "light"
    
    # Force dark si fond sombre détecté
    if theme == "dark":
        return {
            'text': '#F5F5F5',  # Blanc cassé pour bien voir
            'grid': '#555', 
            'spine': '#777777',
            'bar': '#64B5F6',   # Bleu clair pour dark
            'pie': ['#64B5F6', '#FFB74D', '#81C784', '#BA68C8']
        }
    else:
        return {
            'text': '#0A1F44',  # Bleu marine pour light
            'grid': '#E0E0E0',
            'spine': '#E0E0E0', 
            'bar': '#1976D2',   # Bleu foncé pour light
            'pie': ['#1976D2', '#FF7043', '#26A69A', '#7E57C2']
        }
def graphique_services(df):
    colors = get_theme_colors()
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Fond transparent pour flotter dans la card
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    df['Service'].value_counts().plot(
        kind='barh', ax=ax, color=colors['bar'], edgecolor='none'
    )
    
    ax.set_title('Fréquentation par service', fontsize=14, fontweight='bold', color=colors['text'], pad=20)
    ax.set_xlabel('Nombre de patients', color=colors['text'])
    ax.set_ylabel('', color=colors['text'])
    ax.tick_params(colors=colors['text'], labelsize=10)
    
    for spine in ax.spines.values():
        spine.set_color(colors['spine'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', color=colors['grid'], alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    return fig

def graphique_sexe(df):
    colors = get_theme_colors()
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    sexe_counts = df['Sexe'].value_counts()
    wedges, texts, autotexts = ax.pie(
        sexe_counts.values, 
        labels=sexe_counts.index,
        autopct='%1.1f%%',
        colors=colors['pie'][:len(sexe_counts)],
        startangle=90,
        textprops={'color': colors['text'], 'fontsize': 11}
    )
    
    ax.set_title('Répartition par sexe', fontsize=14, fontweight='bold', color=colors['text'], pad=20)
    plt.tight_layout()
    return fig

def graphique_diagnostics(df):
    colors = get_theme_colors()
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    top_diag = df['Diagnostic'].value_counts().head(10)
    top_diag.plot(kind='barh', ax=ax, color=colors['bar'])
    
    ax.set_title('Top 10 des diagnostics', fontsize=14, fontweight='bold', color=colors['text'], pad=20)
    ax.set_xlabel('Nombre de cas', color=colors['text'])
    ax.set_ylabel('Diagnostics', color=colors['text'])
    ax.tick_params(colors=colors['text'])
    
    for spine in ax.spines.values():
        spine.set_color(colors['spine'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', color=colors['grid'], alpha=0.3)
    
    plt.tight_layout()
    return fig

def graphique_statuts(df):
    colors = get_theme_colors()
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    statut_counts = df['Statut'].value_counts()
    wedges, texts, autotexts = ax.pie(
        statut_counts.values,
        labels=statut_counts.index,
        autopct='%1.1f%%',
        colors=colors['pie'][:len(statut_counts)],
        startangle=90,
        textprops={'color': colors['text'], 'fontsize': 11, 'fontweight': '500'}
    )
    
    ax.set_title('Répartition des statuts', fontsize=14, fontweight='bold', color=colors['text'], pad=20)
    plt.tight_layout()
    return fig

def histogramme_ages(df):
    colors = get_theme_colors()
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    ax.hist(df['Age'], bins=20, color=colors['bar'], edgecolor='none', alpha=0.8)
    
    ax.set_title('Distribution des âges', fontsize=14, fontweight='bold', color=colors['text'], pad=20)
    ax.set_xlabel('Âge', color=colors['text'])
    ax.set_ylabel('Fréquence', color=colors['text'])
    ax.tick_params(colors=colors['text'])
    
    for spine in ax.spines.values():
        spine.set_color(colors['spine'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', color=colors['grid'], alpha=0.3)
    
    plt.tight_layout()
    return fig
def graphique_heatmap(df):
    """Heatmap fréquentation par jour et heure - Style ESI"""
    if 'Date' not in df.columns or df['Date'].isna().all():
        return None

    # Assure que Date est datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Extrait jour + heure
    df['Jour'] = df['Date'].dt.day_name()
    df['Heure'] = df['Date'].dt.hour

    # Pivot table: Jours en lignes, Heures en colonnes
    heatmap_data = df.pivot_table(
        index='Jour',
        columns='Heure',
        aggfunc='size',  # <- CORRECTION ICI
        fill_value=0
    )
def statistiques_generales(df):
	stats = {
	'total_patients': len(df),
	'nb_services': df['Service'].nunique() if 'Service' in df.columns else 0,
	'sexe_repartition': df['Sexe'].value_counts().to_dict() if 'Sexe' in df.columns else {},
	'statut_repartition': df['Statut'].value_counts().to_dict() if 'Statut' in df.columns else {}
	}
	return stats
