# app.py
import streamlit as st
import pandas as pd
import io
import time
import base64
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate,Table, TableStyle,paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
from reportlab.lib import colors
from src.utils import *
from src.analyse import *
from src.visualisation import *
from reportlab.lib.utils import ImageReader
# Palette ESI officielle
ESI_COLORS = ['#0A1F44', '#64B5F6', '#90CAF9', '#42A5F5', '#1E88E5', '#1976D2']

# Template global Plotly ESI
import plotly.io as pio
pio.templates["esi"] = pio.templates["plotly_white"]
pio.templates["esi"].layout.colorway = ESI_COLORS
pio.templates["esi"].layout.font.family = "Poppins"
pio.templates["esi"].layout.title.font.color = "#0A1F44"
pio.templates["esi"].layout.xaxis.title.font.color = "#0A1F44"
pio.templates["esi"].layout.yaxis.title.font.color = "#0A1F44"
pio.templates["esi"].layout.plot_bgcolor = "white"
pio.templates["esi"].layout.paper_bgcolor = "white"
pio.templates.default = "esi"

# Animation démarrage qui disparaît
placeholder = st.empty()

with placeholder.status("🚀 Initialisation du Dashboard ESI...", expanded=True) as status:
    time.sleep(1)
    st.write("Chargement des modules...")
    time.sleep(0.3)
    st.write("Connexion à l’interface...")
    time.sleep(0.3)
    status.update(label="✅ Prêt!", state="complete")
    time.sleep(1.5)  # Laisse 1.5sec pour voir le check vert

placeholder.empty()  # 👈 BOOM il disparaît complètement
# --------------------------------------------------
# Configuration de la page
# --------------------------------------------------

col_logo, col_titre = st.columns([1,5])

with col_logo:
    st.image("logo01.png", width=100)

with col_titre:
    st.markdown("## ECOLE SUPERIEURE D'INFORMATIQUE /UNIKOL")
    st.caption("Analyse des données de fréquentation des services de santé")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif;
}

/* Boutons ESI */
.stButton > button {
    background: linear-gradient(135deg, #0A1F44 0%, #64B5F6 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    transition: 0.3s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(10, 31, 68, 0.3);
}

/* Sidebar ESI - fond bleu nuit */
[data-testid="stSidebar"] {
    background: #0A1F44;
}

/* 1. Titre "Filtres" + st.info = BLANC */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] .stAlert div {
    color: white !important;
}

/* 2. Labels Service/Sexe/Statut = BLEU ESI */
section[data-testid="stSidebar"] .stSelectbox label {
    color: #64B5F6 !important;
    font-weight: 600;
    font-size: 15px;
}

/* 3. Selectbox bordure */
.stSelectbox div[data-baseweb="select"] {
    border-color: #64B5F6 !important;
}

/* 4. Valeur sélectionnée "Tous, Consultation..." = NOIR */
section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: black !important;
}

/* 5. Options dans la liste déroulante = NOIR sur BLANC */
[data-baseweb="popover"] [role="listbox"] [role="option"] {
    color: black !important;
    background-color: white !important;
}

/* 6. Hover option */
[data-baseweb="popover"] [role="listbox"] [role="option"]:hover {
    background-color: #E3F2FD !important;
    color: black !important;
}

/* Métriques KPI */
[data-testid="stMetricValue"] {
    color: #0A1F44 !important;
    font-weight: 700;
}
[data-testid="stMetricLabel"] {
    color: #64B5F6 !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CSS + Header Pro style site web
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;600&family=Poppins:wght@400;500;600&display=swap');

.main { background-color:#F5F7FA; }

/* Hero Header */
.hero {
    background: linear-gradient(135deg, #0A1F44 0%, #1E4D8C 50%, #1976D2 100%);
    padding: 70px 50px;
    border-radius: 20px;
    margin-bottom: 35px;
    box-shadow: 0 12px 35px rgba(10, 31, 68, 0.25);
}
.hero h1 {
    font-family: 'Montserrat', sans-serif;
    font-size: 58px;
    font-weight: 700;
    color: white;
    margin: 0;
    line-height: 1.2;
    letter-spacing: -1px;
}
.hero .subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    color: #64B5F6;
    margin-top: 15px;
    font-weight: 400;
}
.hero .badge {
    display: inline-block;
    background: rgba(100, 181, 246, 0.18);
    border: 1px solid #64B5F6;
    color: #64B5F6;
    padding: 8px 18px;
    border-radius: 25px;
    font-size: 14px;
    margin-bottom: 25px;
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
}
.underline {
    width: 140px;
    height: 4px;
    background: #64B5F6;
    border-radius: 2px;
    margin-top: 25px;
}

/* Cards pour metrics et graphiques */
[data-testid="stMetric"] {
    background: white;
    padding: 25px 20px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    border: 1px solid #E3F2FD;
    transition: transform 0.2s;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(30, 77, 140, 0.15);
}

/* Titres de section */
h2, h3 {
    font-family: 'Montserrat', sans-serif !important;
    color: #0A1F44 !important;
    font-weight: 600 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] { background-color: #0A1F44; }
section[data-testid="stSidebar"] .stSelectbox label {
    color: #64B5F6 !important;
    font-weight: 500;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: white;
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
    border-radius: 8px;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1E4D8C 0%, #1976D2 100%);
    color: white !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    border: 1px solid #E3F2FD;
}

/* Footer */
.footer {
    text-align: center;
    color: #78909C;
    padding: 30px 0;
    font-family: 'Poppins', sans-serif;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

#col1, col2 = st.columns([1, 5])
#with col1:
    #st.image("logo01.png", width=85)
#with col2:
    #st.markdown("### HOSPITAL ANALYTICS")
    #st.markdown("Analyse des données de fréquentation des services de santé") 

st.markdown(f"""
<div class="hero">
    <div style="display:flex; align-items:center; gap:25px;">
        <img src="" style="width:85px; height:auto; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1);">
        <div>
            <div class="badge">⚕️ Données Sanitaires RDC</div>
            <h1>HOSPITAL ANALYTICS</h1>
            <p class="subtitle">Analyse des données de fréquentation des services de santé</p>
        </div>
    </div>
    <div class="underline"></div>
    
</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <p style='text-align:center; font-family:Poppins; font-size:16px; color:#546E7A; margin-bottom:40px;'>
    Cette application permet d'analyser les données de fréquentation des services de santé 
    afin de soutenir la prise de décision dans les structures hospitalières locales.
    </p>
   
    """,
    unsafe_allow_html=True
)

# Fonction animation KPIs
def animate_metric(col, label, final_value, suffix=""):
    if f"anim_done_{label}" not in st.session_state:
        st.session_state[f"anim_done_{label}"] = False
    
    placeholder = col.empty()
    
    if st.session_state[f"anim_done_{label}"]:
        val = f"{final_value:.1f}{suffix}" if isinstance(final_value, float) else f"{final_value}{suffix}"
        placeholder.metric(label, val)
        return
    
    steps = 25
    for i in range(steps + 1):
        if isinstance(final_value, float):
            current = final_value * i / steps
            placeholder.metric(label, f"{current:.1f}{suffix}")
        else:
            current = int(final_value * i / steps)
            placeholder.metric(label, f"{current}{suffix}")
        time.sleep(0.015)
    
    st.session_state[f"anim_done_{label}"] = True

# --------------------------------------------------
# Barre latérale
# --------------------------------------------------
st.sidebar.title("⚙️ Filtres")
st.sidebar.info("Utilisez les filtres pour explorer les données.")

# --------------------------------------------------
# Importation du fichier
# --------------------------------------------------
fichier = st.file_uploader("Importer le fichier Excel", type=["xlsx"])

# --------------------------------------------------
# Traitement
# --------------------------------------------------
if fichier:
    df = charger_donnees(fichier)
    df = nettoyer_donnees(df)

    # Filtres
    services = ["Tous"] + sorted(df["Service"].unique().tolist())
    service_selectionne = st.sidebar.selectbox("Service", services)
    if service_selectionne != "Tous":
        df = df[df["Service"] == service_selectionne]

    sexes = ["Tous"] + sorted(df["Sexe"].unique().tolist())
    sexe_selectionne = st.sidebar.selectbox("Sexe", sexes)
    if sexe_selectionne != "Tous":
        df = df[df["Sexe"] == sexe_selectionne]

    statuts = ["Tous"] + sorted(df["Statut"].unique().tolist())
    statut_selectionne = st.sidebar.selectbox("Statut", statuts)
    if statut_selectionne != "Tous":
        df = df[df["Statut"] == statut_selectionne]

        # ===== LOADER PRO ESI =====
    loader_placeholder = st.empty()

    with loader_placeholder.container():
        st.markdown("""
        <style>
        .loader-box {
            background: linear-gradient(135deg, #0A1F44 0%, #1E4D8C 100%);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 8px 25px rgba(10, 31, 68, 0.2);
        }
        .loader-text {
            color: white;
            font-family: 'Poppins', sans-serif;
            font-size: 1.1rem;
            font-weight: 500;
            margin-top: 1rem;
        }
        .loader-dots span {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #64B5F6;
            margin: 0 4px;
            animation: bounce 1.4s infinite ease-in-out;
        }
        .loader-dots span:nth-child(1) { animation-delay: -0.32s; }
        .loader-dots span:nth-child(2) { animation-delay: -0.16s; }
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        </style>
        
        <div class="loader-box">
            <div class="loader-dots">
                <span></span><span></span><span></span>
            </div>
            <div class="loader-text">Traitement des données en cours...</div>
        </div>
        """, unsafe_allow_html=True)

    # Simule le temps de traitement
    import time
        # Loader 3 secondes avec progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(100):
        time.sleep(0.03)  # 0.03 * 100 = 3 secondes
        progress_bar.progress(i + 1)
        status_text.markdown(f"<p style='text-align:center; color:#64B5F6; font-family:Poppins;'>Traitement... {i+1}%</p>", unsafe_allow_html=True)

    progress_bar.empty()
    status_text.empty()
    stats = statistiques_generales(df)
        # Supprime le loader
    loader_placeholder.empty()
    st.success("✅ Analyse terminée avec succès")
    # ===== FIN LOADER =====

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Tableau de bord", "📈 Analyses", "📥 Exportation"])

    with tab1:
        st.subheader("📋 Aperçu des données")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.info(generer_conclusion(df, stats))
        st.markdown("---")
        st.subheader("🔍 Détection d'Anomalies")
        anomalie_msg = detecter_anomalies(df)
        if "⚠️" in anomalie_msg:
            st.error(anomalie_msg)
        else:
            st.success(anomalie_msg)

        col1, col2, col3, col4 = st.columns(4, gap="large")
        animate_metric(col1, "👥 Patients", stats["Nombre total de patients"])
        animate_metric(col2, "🎂 Âge moyen", stats["Age moyen"])
        animate_metric(col3, "⏱ Temps attente", stats["Temps d\'attente moyen"], " min")
        animate_metric(col4, "🏥 Services", df["Service"].nunique())
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        # 👇 COLLE ÇA ICI, SANS INDENTATION, JUSTE APRÈS LES KPI
        st.subheader("🎯 Top 5 Insights Automatiques")
        analyse = analyse_avancee(df)
        insights = generer_top5_insights(df, stats, analyse)

        cols1 = st.columns(3) # Ligne 1 : 3 cartes
        cols2 = st.columns(3) # Ligne 2 : 2 cartes + 1 vide

        for i, insight in enumerate(insights):
            if i < 3:
                with cols1[i]:
                    st.markdown(f"""<div style="background: linear-gradient(135deg, {insight['couleur']}15, white); border-left: 4px solid {insight['couleur']}; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 170px;"><div style="font-size: 24px;">{insight['icone']}</div><div style="font-size: 12px; color: gray; font-weight: 600;">{insight['titre']}</div><div style="font-size: 22px; font-weight: bold; color: #0A1F44; margin: 5px 0;">{insight['valeur']}</div><div style="font-size: 11px; color: #555;">{insight['desc']}</div></div>""", unsafe_allow_html=True)
            else:
                with cols2[i-3]:
                    st.markdown(f"""<div style="background: linear-gradient(135deg, {insight['couleur']}15, white); border-left: 4px solid {insight['couleur']}; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); height: 170px;"><div style="font-size: 24px;">{insight['icone']}</div><div style="font-size: 12px; color: gray; font-weight: 600;">{insight['titre']}</div><div style="font-size: 22px; font-weight: bold; color: #0A1F44; margin: 5px 0;">{insight['valeur']}</div><div style="font-size: 11px; color: #555;">{insight['desc']}</div></div>""", unsafe_allow_html=True)
                # Score juste après
                score = calculer_score_hospitalier(stats, df)
                col_score1, col_score2 = st.columns([1, 2])
                

        
        with col_score2:
            st.plotly_chart(graphique_score(score), use_container_width=True,key="score_jauge_unique")

    with tab2:
        st.subheader("📊 Fréquentation par service")
        fig1 = graphique_services(df)
        st.pyplot(fig1)

        st.subheader("👨‍⚕️ Répartition par sexe")
        fig2 = graphique_sexe(df)
        st.pyplot(fig2)

        st.subheader("🩺 Top diagnostics")
        fig3 = graphique_diagnostics(df)
        st.pyplot(fig3)

        st.subheader("📋 Répartition des statuts")
        fig4 = graphique_statuts(df)
        st.pyplot(fig4)

        st.subheader("📊 Distribution des âges")
        fig5 = histogramme_ages(df)
        st.pyplot(fig5)
        
        st.markdown("---")
        st.subheader("🗓️ Analyse Temporelle")
        heatmap_fig = graphique_heatmap(df)
        if heatmap_fig:
            st.plotly_chart(heatmap_fig, use_container_width=True)
            st.caption("💡 Zones bleu nuit = heures de pic. Zones bleu clair = creux d'activité")
        else:
            st.info("Ajoute une colonne 'Date' avec heure pour activer la heatmap")
            
    with tab3:
        st.subheader("📥 Exportation des données")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📄 Télécharger CSV",
            data=csv,
            file_name="rapport_hospitalier.csv",
            mime="text/csv"
        )

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Donnees")
        st.download_button(
            label="📊 Télécharger Excel",
            data=buffer.getvalue(),
            file_name="rapport_hospitalier.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # PDF Pro avec bandeau bleu + logo
        pdf_buffer = io.BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
        width, height = A4

        BLUE_DARK = HexColor("#0A1F44")
        BLUE_LIGHT = HexColor("#64B5F6")

        # Bandeau header
        pdf.setFillColor(BLUE_DARK)
        pdf.rect(0, height-100, width, 100, fill=1, stroke=0)

        # Logo dans bandeau
        from reportlab.lib.utils import ImageReader
        pdf.drawImage(ImageReader("logo01.png"), 40, height-90, width=70, height=70, mask='auto')

        # Titre
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(130, height-50, "RAPPORT HOSPITAL ANALYTICS")
        pdf.setFont("Helvetica", 11)
        pdf.setFillColor(BLUE_LIGHT)
        pdf.drawString(130, height-70, "Analyse des données de fréquentation | UNIKOL")

        # Date
        pdf.setFillColor(HexColor("#000"))
        pdf.setFont("Helvetica", 10)
        pdf.drawString(40, height-130, f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        # Tableau KPIs
        data = [
            ["Indicateur", "Valeur"],
            ["Nombre total de patients", f"{stats['Nombre total de patients']}"],
            ["Âge moyen", f"{stats['Age moyen']} ans"],
            ["Temps d'attente moyen", f"{stats['Temps d\'attente moyen']} min"],
            ["Nombre de services", f"{df['Service'].nunique()}"]
        ]

        table = Table(data, colWidths=[300, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), BLUE_DARK),
            ('TEXTCOLOR', (0,0), (-1,0), HexColor("#FFFFFF")),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), HexColor("#F5F7FA")),
            ('GRID', (0,0), (-1,-1), 1, BLUE_LIGHT),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 11),
        ]))
        table.wrapOn(pdf, width, height)
        table.drawOn(pdf, 40, height-300)

        # Footer
        pdf.setFont("Helvetica-Oblique", 9)
        pdf.setFillColor(HexColor("#78909C"))
        pdf.drawCentredString(width/2, 30, "Université de Kolwezi | Réseau et Télécommunications | 2025-2026")

        # Section Analyse + Score dans PDF
        pdf.setFillColor(HexColor("#0A1F44"))
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(40, height-350, "ANALYSE & RECOMMANDATIONS")

        # Conclusion auto
        pdf.setFillColor(HexColor("#000"))
        pdf.setFont("Helvetica", 10)
        text_obj = pdf.beginText(40, height-370)
        text_obj.setLeading(14)  # interligne

        conclusion_texte = generer_conclusion(df, stats).replace('**', '')
        for line in conclusion_texte.split('\n'):
            text_obj.textLine(line.strip())

        # Ajout Score
        text_obj.textLine("")
        text_obj.textLine(f"Score Performance Hôpital: {score}/100 - {'Excellent' if score>=80 else 'Moyen' if score>=50 else 'Critique'}")
        pdf.drawText(text_obj)
        pdf.save()
        pdf_buffer.seek(0)

        st.download_button(
            label="📄 Télécharger PDF Pro",
            data=pdf_buffer.getvalue(),
            file_name="rapport_hospitalier_pro.pdf",
            mime="application/pdf"
        )

    st.markdown('<div class="footer">Application développée dans le cadre du mémoire<br>Université de Kolwezi | Réseau et Télécommunications<br>Année académique 2025-2026</div>', unsafe_allow_html=True)
    st.markdown(
    """
    <p style='text-align:center; font-family:Poppins; font-size:16px; color:#546E7A; margin-bottom:40px;'>
    © Gloire Kayembe 2026 - Tous droits réservés
    
   
    """,
    unsafe_allow_html=True
)
else:
    st.info("👆 Veuillez importer un fichier Excel pour commencer l'analyse.")