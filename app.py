import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime, timezone, timedelta

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Bolão do Bobão — Copa 2026",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* ── Reset mobile ── */
.main .block-container {
    padding-top: 0.75rem;
    padding-bottom: 3rem;
    padding-left: 12px;
    padding-right: 12px;
    max-width: 680px;
}

/* ── Tipografia ── */
h1 { font-size: 22px !important; font-weight: 800 !important; text-align: center;
     letter-spacing: -0.5px; color: #1e3a5f !important; margin-bottom: 2px !important; }
h2 { font-size: 16px !important; font-weight: 700 !important; color: #1e3a5f !important;
     margin-top: 18px !important; margin-bottom: 6px !important; }
h3 { font-size: 14px !important; font-weight: 600 !important; color: #334155 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 3px; background: #f1f5f9; padding: 4px;
    border-radius: 10px; }
.stTabs [data-baseweb="tab"] {
    font-size: 12px !important; font-weight: 600 !important;
    padding: 7px 10px !important; border-radius: 7px !important;
    background: transparent !important; color: #64748b !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #1e3a5f !important; color: #ffffff !important;
}

/* ── Cards de grupo ── */
.group-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 12px 14px; margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.group-header {
    font-weight: 700; background: #1e3a5f; color: white;
    padding: 5px 12px; border-radius: 7px; margin-bottom: 10px;
    font-size: 13px; text-align: center;
}
.group-header-br {
    font-weight: 700; background: #15803d; color: white;
    padding: 5px 12px; border-radius: 7px; margin-bottom: 10px;
    font-size: 13px; text-align: center;
}

/* ── Status e alertas ── */
.status-travado {
    background: #dcfce7; border-left: 4px solid #16a34a;
    padding: 10px 14px; border-radius: 8px; color: #14532d;
    font-weight: 700; font-size: 13px; text-align: center;
    margin-bottom: 14px;
}
.status-editando {
    background: #fef9c3; border-left: 4px solid #ca8a04;
    padding: 10px 14px; border-radius: 8px; color: #713f12;
    font-weight: 600; font-size: 13px; margin-bottom: 14px;
}

/* ── Caixa de confirmação ── */
.cuzao-box {
    background: #fff1f2; border: 2px solid #e11d48;
    padding: 16px; border-radius: 12px; text-align: center; margin: 12px 0;
}
.cuzao-title { color: #be123c !important; font-weight: 700 !important;
               font-size: 15px !important; margin: 0 0 6px !important; }
.cuzao-sub   { color: #3f3f46; font-size: 13px; font-weight: 500; margin: 0; }

/* ── Calendário ── */
.jogo-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 10px 13px; margin-bottom: 8px;
    display: flex; align-items: center; gap: 10px;
}
.jogo-data { font-size: 11px; color: #64748b; min-width: 36px; text-align: center; }
.jogo-hora { font-size: 11px; font-weight: 700; color: #334155; min-width: 34px; }
.jogo-nome { font-size: 13px; font-weight: 600; color: #1e293b; flex: 1; }
.jogo-local { font-size: 11px; color: #94a3b8; }
.badge-finalizado { background: #dcfce7; color: #15803d; font-size: 10px;
    font-weight: 700; padding: 2px 7px; border-radius: 20px; white-space: nowrap; }
.badge-aovivo { background: #fef2f2; color: #dc2626; font-size: 10px;
    font-weight: 700; padding: 2px 7px; border-radius: 20px; white-space: nowrap;
    animation: pulse-badge 1.5s ease-in-out infinite; }
.badge-previsto { background: #f1f5f9; color: #64748b; font-size: 10px;
    font-weight: 600; padding: 2px 7px; border-radius: 20px; white-space: nowrap; }
@keyframes pulse-badge {
    0%, 100% { opacity: 1; } 50% { opacity: 0.6; }
}
.data-header {
    font-size: 12px; font-weight: 700; color: #475569;
    background: #f8fafc; padding: 5px 12px; border-radius: 6px;
    margin: 10px 0 6px; border-left: 3px solid #1e3a5f;
}
.jogo-brasil { border-left: 3px solid #15803d !important; }

/* ── Countdown ── */
.countdown-box {
    background: linear-gradient(135deg, #1e3a5f 0%, #1d4ed8 100%);
    color: white; border-radius: 12px; padding: 12px 16px;
    text-align: center; margin-bottom: 16px;
}
.countdown-label { font-size: 11px; font-weight: 600; opacity: 0.8;
    text-transform: uppercase; letter-spacing: 0.05em; }
.countdown-time  { font-size: 22px; font-weight: 800; letter-spacing: 1px; }
.countdown-game  { font-size: 12px; opacity: 0.85; margin-top: 2px; }

/* ── Ranking ── */
.rank-row {
    display: flex; align-items: center; gap: 10px;
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 10px 13px; margin-bottom: 7px;
}
.rank-pos { font-size: 18px; font-weight: 800; min-width: 28px; color: #1e3a5f; }
.rank-nome { font-size: 14px; font-weight: 700; color: #1e293b; flex: 1; }
.rank-pts { font-size: 20px; font-weight: 800; color: #1e3a5f; min-width: 40px; text-align: right; }
.rank-pts-label { font-size: 10px; color: #94a3b8; text-align: right; }
.rank-badges { font-size: 12px; color: #64748b; }
.rank-status-open { color: #ca8a04; font-size: 11px; font-weight: 600; }
.rank-status-lock { color: #16a34a; font-size: 11px; font-weight: 600; }

/* ── PIN ── */
.pin-box {
    background: #f8fafc; border: 1.5px solid #cbd5e1;
    border-radius: 12px; padding: 20px; text-align: center; margin: 12px 0;
}

/* ── Modo view-only ── */
.view-banner {
    background: #eff6ff; border: 1px solid #bfdbfe;
    border-radius: 8px; padding: 9px 14px; font-size: 13px;
    color: #1d4ed8; font-weight: 600; margin-bottom: 14px; text-align: center;
}

/* ── Mata-mata cards ── */
.mm-fase-header {
    font-size: 15px; font-weight: 800; color: #fff;
    background: linear-gradient(90deg, #1e3a5f, #1d4ed8);
    padding: 8px 16px; border-radius: 10px; margin: 18px 0 10px; text-align: center;
}
.mm-fase-locked {
    background: #f1f5f9; border: 1px dashed #cbd5e1;
    border-radius: 10px; padding: 12px; text-align: center;
    color: #94a3b8; font-size: 13px; font-weight: 600; margin-bottom: 12px;
}
.mm-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 12px 14px; margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.mm-id { font-size: 10px; color: #94a3b8; font-weight: 700;
    text-transform: uppercase; margin-bottom: 4px; letter-spacing: 0.05em; }
.mm-times { font-size: 13px; font-weight: 700; color: #334155; margin-bottom: 6px; }
.mm-real-result {
    background: #f0f9ff; border-left: 3px solid #0284c7;
    border-radius: 6px; padding: 5px 10px; margin-top: 6px;
    font-size: 12px; color: #0c4a6e; font-weight: 600;
}

/* ── Fonte de dados ── */
.fonte-dados {
    font-size: 11px; color: #94a3b8; text-align: right;
    margin-bottom: 4px; font-style: italic;
}

/* ── Inputs ── */
.stNumberInput input { font-size: 16px !important; text-align: center !important; }
.stButton > button { width: 100%; border-radius: 8px; height: 2.8rem;
    font-weight: 700; font-size: 14px; }
.stSelectbox label { font-size: 13px !important; }

/* ── Regras de pontuação ── */
.regra-box {
    background: #f0f9ff; border: 1px solid #bae6fd;
    border-radius: 10px; padding: 12px 14px; margin-bottom: 14px;
}
.regra-item { font-size: 13px; color: #0c4a6e; padding: 3px 0; }
.real-box {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 8px 10px; margin-top: 8px;
    font-size: 12px; color: #334155;
}
.real-title { font-weight: 800; color: #1e3a5f; margin-bottom: 3px; }
.real-line { padding: 2px 0; }
.detail-ok { color: #15803d; font-weight: 700; }
.detail-err { color: #be123c; font-weight: 700; }
.detail-wait { color: #64748b; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DADOS FIXOS
# ==============================================================================
AMIGOS = ["Fefo", "Vini", "Nico", "Bruno", "Renan", "Juan"]

GRUPOS_CONFIG = {
    "Grupo A": ["Tchéquia", "México", "África do Sul", "República da Coreia"],
    "Grupo B": ["Bósnia e Herzegovina", "Canadá", "Catar", "Suíça"],
    "Grupo C": ["Brasil", "Haiti", "Marrocos", "Escócia"],
    "Grupo D": ["Austrália", "Paraguai", "Turquia", "Estados Unidos"],
    "Grupo E": ["Curaçao", "Equador", "Alemanha", "Costa do Marfim"],
    "Grupo F": ["Japão", "Países Baixos", "Suécia", "Tunísia"],
    "Grupo G": ["Bélgica", "Egito", "Irã", "Nova Zelândia"],
    "Grupo H": ["Cabo Verde", "Arábia Saudita", "Espanha", "Uruguai"],
    "Grupo I": ["França", "Iraque", "Noruega", "Senegal"],
    "Grupo J": ["Argélia", "Argentina", "Áustria", "Jordânia"],
    "Grupo K": ["Colômbia", "RD Congo", "Portugal", "Uzbequistão"],
    "Grupo L": ["Croácia", "Inglaterra", "Gana", "Panamá"],
}

JOGOS_BRASIL = [
    {"rodada": 1, "jogo": "Brasil x Marrocos",  "data": "13/06", "hora": "19h00", "loc": "Nova York/NJ"},
    {"rodada": 2, "jogo": "Brasil x Haiti",      "data": "19/06", "hora": "21h30", "loc": "Filadélfia"},
    {"rodada": 3, "jogo": "Escócia x Brasil",    "data": "24/06", "hora": "19h00", "loc": "Miami"},
]

# ==============================================================================
# MATA-MATA — estrutura por fase com placeholders que viram nomes reais
# ==============================================================================
'''
MATA_MATA_16AVOS_REAL = [
    # id, time1, time2, data, hora, local
    {"id": "R1",  "t1": "África do Sul",      "t2": "Canadá",            "data": "28/06", "hora": "16h00", "local": "Los Angeles"},
    {"id": "R2",  "t1": "Brasil",              "t2": "Japão",             "data": "29/06", "hora": "14h00", "local": "Houston"},
    {"id": "R3",  "t1": "Alemanha",            "t2": "Paraguai",          "data": "29/06", "hora": "17h30", "local": "Boston"},
    {"id": "R4",  "t1": "Países Baixos",       "t2": "Marrocos",          "data": "29/06", "hora": "22h00", "local": "Monterrey"},
    {"id": "R5",  "t1": "Costa do Marfim",     "t2": "Noruega",           "data": "30/06", "hora": "14h00", "local": "Dallas"},
    {"id": "R6",  "t1": "França",              "t2": "Suécia",            "data": "30/06", "hora": "18h00", "local": "Nova Jersey"},
    {"id": "R7",  "t1": "México",              "t2": "Equador",           "data": "30/06", "hora": "22h00", "local": "Cidade do México"},
    {"id": "R8",  "t1": "Inglaterra",          "t2": "RD Congo",          "data": "01/07", "hora": "13h00", "local": "Atlanta"},
    {"id": "R9",  "t1": "Bélgica",             "t2": "Senegal",           "data": "01/07", "hora": "17h00", "local": "Seattle"},
    {"id": "R10", "t1": "Estados Unidos",      "t2": "Bósnia e Herzegovina", "data": "01/07", "hora": "21h00", "local": "Santa Clara"},
    {"id": "R11", "t1": "Espanha",             "t2": "Áustria",           "data": "02/07", "hora": "16h00", "local": "Los Angeles"},
    {"id": "R12", "t1": "Croácia",             "t2": "Portugal",          "data": "02/07", "hora": "20h00", "local": "Toronto"},
    {"id": "R13", "t1": "Suíça",               "t2": "Argélia",           "data": "03/07", "hora": "00h00", "local": "Vancouver"},
    {"id": "R14", "t1": "Austrália",           "t2": "Egito",             "data": "03/07", "hora": "15h00", "local": "Dallas"},
    {"id": "R15", "t1": "Argentina",           "t2": "Cabo Verde",        "data": "03/07", "hora": "19h00", "local": "Miami"},
    {"id": "R16", "t1": "Colômbia",            "t2": "Gana",              "data": "03/07", "hora": "22h30", "local": "Kansas City"},
]

# Oitavas: vencedores de pares de R1-R16
# R1 vs R2 → Q1
# R3 vs R4 → Q2
# R5 vs R6 → Q3
# R7 vs R8 → Q4
# R9 vs R10 → Q5
# R11 vs R12 → Q6
# R13 vs R14 → Q7
# R15 vs R16 → Q8
MATA_MATA_OITAVAS_REAL = [
    {"id": "O1", "t1": "Venc. R1", "t2": "Venc. R2"},  # AFS/CAN vs BRA/JPN
    {"id": "O2", "t1": "Venc. R3", "t2": "Venc. R4"},  # ALE/PAR vs HOL/MAR
    {"id": "O3", "t1": "Venc. R5", "t2": "Venc. R6"},  # CIV/NOR vs FRA/SUE
    {"id": "O4", "t1": "Venc. R7", "t2": "Venc. R8"},  # MEX/EQU vs ING/RDC
    {"id": "O5", "t1": "Venc. R9", "t2": "Venc. R10"}, # BEL/SEN vs EUA/BOS
    {"id": "O6", "t1": "Venc. R11","t2": "Venc. R12"}, # ESP/AUS vs CRO/POR
    {"id": "O7", "t1": "Venc. R13","t2": "Venc. R14"}, # SUI/ALG vs AUS/EGI
    {"id": "O8", "t1": "Venc. R15","t2": "Venc. R16"}, # ARG/CAB vs COL/GAN
]

MATA_MATA_QUARTAS_REAL = [
    {"id": "Q1", "t1": "Venc. O1", "t2": "Venc. O2"},
    {"id": "Q2", "t1": "Venc. O3", "t2": "Venc. O4"},
    {"id": "Q3", "t1": "Venc. O5", "t2": "Venc. O6"},
    {"id": "Q4", "t1": "Venc. O7", "t2": "Venc. O8"},
]

MATA_MATA_SEMIS_REAL = [
    {"id": "S1", "t1": "Venc. Q1", "t2": "Venc. Q2"},
    {"id": "S2", "t1": "Venc. Q3", "t2": "Venc. Q4"},
]

MATA_MATA_FINAL_REAL = [
    {"id": "T1", "t1": "Perd. S1", "t2": "Perd. S2", "label": "🥉 3º Lugar"},
    {"id": "F1", "t1": "Venc. S1", "t2": "Venc. S2", "label": "🏆 FINAL"},
]
'''
# Chaveamento fixo das oitavas (posições dos grupos)
# Quando a classificação final de grupos estiver disponível, os nomes reais
# serão resolvidos automaticamente via _resolver_nome_mm()
MATA_MATA_OITAVAS_DEF = [
    {"id": "M1",  "pos1": ("E", 1), "pos2": ("?", 0)},   # 1ºE vs 3º colocado
    {"id": "M2",  "pos1": ("I", 1), "pos2": ("?", 0)},   # 1ºI vs 3º colocado
    {"id": "M3",  "pos1": ("A", 2), "pos2": ("B", 2)},   # 2ºA vs 2ºB
    {"id": "M4",  "pos1": ("F", 1), "pos2": ("C", 2)},   # 1ºF vs 2ºC
    {"id": "M5",  "pos1": ("K", 2), "pos2": ("L", 2)},   # 2ºK vs 2ºL
    {"id": "M6",  "pos1": ("H", 1), "pos2": ("J", 2)},   # 1ºH vs 2ºJ
    {"id": "M7",  "pos1": ("D", 1), "pos2": ("?", 0)},   # 1ºD vs 3º colocado
    {"id": "M8",  "pos1": ("G", 1), "pos2": ("?", 0)},   # 1ºG vs 3º colocado
    {"id": "M9",  "pos1": ("C", 1), "pos2": ("F", 2)},   # 1ºC vs 2ºF
    {"id": "M10", "pos1": ("E", 2), "pos2": ("I", 2)},   # 2ºE vs 2ºI
    {"id": "M11", "pos1": ("A", 1), "pos2": ("?", 0)},   # 1ºA vs 3º colocado
    {"id": "M12", "pos1": ("L", 1), "pos2": ("?", 0)},   # 1ºL vs 3º colocado
    {"id": "M13", "pos1": ("J", 1), "pos2": ("H", 2)},   # 1ºJ vs 2ºH
    {"id": "M14", "pos1": ("D", 2), "pos2": ("G", 2)},   # 2ºD vs 2ºG
    {"id": "M15", "pos1": ("B", 1), "pos2": ("?", 0)},   # 1ºB vs 3º colocado
    {"id": "M16", "pos1": ("K", 1), "pos2": ("?", 0)},   # 1ºK vs 3º colocado
]

# Rótulos legíveis das posições (para quando não há nome real)
MATA_MATA_OITAVAS_LABELS = [
    {"id": "M1",  "t1": "1º Grupo E",  "t2": "3º colocado"},
    {"id": "M2",  "t1": "1º Grupo I",  "t2": "3º colocado"},
    {"id": "M3",  "t1": "2º Grupo A",  "t2": "2º Grupo B"},
    {"id": "M4",  "t1": "1º Grupo F",  "t2": "2º Grupo C"},
    {"id": "M5",  "t1": "2º Grupo K",  "t2": "2º Grupo L"},
    {"id": "M6",  "t1": "1º Grupo H",  "t2": "2º Grupo J"},
    {"id": "M7",  "t1": "1º Grupo D",  "t2": "3º colocado"},
    {"id": "M8",  "t1": "1º Grupo G",  "t2": "3º colocado"},
    {"id": "M9",  "t1": "1º Grupo C",  "t2": "2º Grupo F"},
    {"id": "M10", "t1": "2º Grupo E",  "t2": "2º Grupo I"},
    {"id": "M11", "t1": "1º Grupo A",  "t2": "3º colocado"},
    {"id": "M12", "t1": "1º Grupo L",  "t2": "3º colocado"},
    {"id": "M13", "t1": "1º Grupo J",  "t2": "2º Grupo H"},
    {"id": "M14", "t1": "2º Grupo D",  "t2": "2º Grupo G"},
    {"id": "M15", "t1": "1º Grupo B",  "t2": "3º colocado"},
    {"id": "M16", "t1": "1º Grupo K",  "t2": "3º colocado"},
]

MATA_MATA_QUARTAS = [
    {"id": "Q1", "t1": "Venc. M1",  "t2": "Venc. M2"},
    {"id": "Q2", "t1": "Venc. M3",  "t2": "Venc. M4"},
    {"id": "Q3", "t1": "Venc. M5",  "t2": "Venc. M6"},
    {"id": "Q4", "t1": "Venc. M7",  "t2": "Venc. M8"},
    {"id": "Q5", "t1": "Venc. M9",  "t2": "Venc. M10"},
    {"id": "Q6", "t1": "Venc. M11", "t2": "Venc. M12"},
    {"id": "Q7", "t1": "Venc. M13", "t2": "Venc. M14"},
    {"id": "Q8", "t1": "Venc. M15", "t2": "Venc. M16"},
]

MATA_MATA_SEMIS = [
    {"id": "S1", "t1": "Venc. Q1", "t2": "Venc. Q2"},
    {"id": "S2", "t1": "Venc. Q3", "t2": "Venc. Q4"},
    {"id": "S3", "t1": "Venc. Q5", "t2": "Venc. Q6"},
    {"id": "S4", "t1": "Venc. Q7", "t2": "Venc. Q8"},
]

MATA_MATA_FINAL = [
    {"id": "T1", "t1": "Perd. S1", "t2": "Perd. S2", "label": "3º Lugar (Chave 1)"},
    {"id": "T2", "t1": "Perd. S3", "t2": "Perd. S4", "label": "3º Lugar (Chave 2)"},
    {"id": "F1", "t1": "Venc. S1/S2", "t2": "Venc. S3/S4", "label": "🏆 FINAL"},
]

MATA_MATA_CONFRONTOS = (
    [{"id": l["id"], "t1": l["t1"], "t2": l["t2"]} for l in MATA_MATA_OITAVAS_LABELS]
    + MATA_MATA_QUARTAS + MATA_MATA_SEMIS + MATA_MATA_FINAL
)

# Controles de fase (altere aqui para abrir fases conforme avança o torneio)
MATA_MATA_LIBERADO  = True   # Oitavas abertas para palpite
QUARTAS_LIBERADAS   = False  # Abre após todos os jogos de oitavas
SEMIS_LIBERADAS     = False
FINAL_LIBERADA      = False

BRT = timezone(timedelta(hours=-3))
DURACAO_JOGO_MIN = 110

PROXIMO_JOGO_BRASIL = {
    "nome":      "Brasil x Marrocos",
    "data_hora": datetime(2026, 6, 13, 19, 0, 0, tzinfo=BRT),
}

# ==============================================================================
# CALENDÁRIO COMPLETO (fallback estático)
# ==============================================================================
CALENDARIO_FIXO = [
    {"data": "11/06", "hora": "16h00", "jogo": "México x África do Sul",      "local": "Cidade do México", "brasil": False},
    {"data": "11/06", "hora": "23h00", "jogo": "Tchéquia x Coreia do Sul",    "local": "Guadalajara",      "brasil": False},
    {"data": "12/06", "hora": "16h00", "jogo": "Canadá x Bósnia",             "local": "Toronto",          "brasil": False},
    {"data": "12/06", "hora": "22h00", "jogo": "Estados Unidos x Paraguai",   "local": "Los Angeles",      "brasil": False},
    {"data": "13/06", "hora": "16h00", "jogo": "Catar x Suíça",               "local": "San Francisco",    "brasil": False},
    {"data": "13/06", "hora": "19h00", "jogo": "Brasil x Marrocos",           "local": "Nova York/NJ",     "brasil": True},
    {"data": "13/06", "hora": "22h00", "jogo": "Haiti x Escócia",             "local": "Boston",           "brasil": False},
    {"data": "14/06", "hora": "01h00", "jogo": "Austrália x Turquia",         "local": "Vancouver",        "brasil": False},
    {"data": "14/06", "hora": "14h00", "jogo": "Alemanha x Curaçao",          "local": "Houston",          "brasil": False},
    {"data": "14/06", "hora": "17h00", "jogo": "Países Baixos x Japão",       "local": "Dallas",           "brasil": False},
    {"data": "14/06", "hora": "20h00", "jogo": "Costa do Marfim x Equador",   "local": "Filadélfia",       "brasil": False},
    {"data": "14/06", "hora": "23h00", "jogo": "Suécia x Tunísia",            "local": "Monterrey",        "brasil": False},
    {"data": "15/06", "hora": "13h00", "jogo": "Espanha x Cabo Verde",        "local": "Atlanta",          "brasil": False},
    {"data": "15/06", "hora": "16h00", "jogo": "Bélgica x Egito",             "local": "Seattle",          "brasil": False},
    {"data": "15/06", "hora": "19h00", "jogo": "Arábia Saudita x Uruguai",    "local": "Miami",            "brasil": False},
    {"data": "15/06", "hora": "22h00", "jogo": "Irã x Nova Zelândia",         "local": "Los Angeles",      "brasil": False},
    {"data": "16/06", "hora": "16h00", "jogo": "França x Senegal",            "local": "Nova York/NJ",     "brasil": False},
    {"data": "16/06", "hora": "19h00", "jogo": "Iraque x Noruega",            "local": "Boston",           "brasil": False},
    {"data": "16/06", "hora": "22h00", "jogo": "Argentina x Argélia",         "local": "Kansas City",      "brasil": False},
    {"data": "17/06", "hora": "01h00", "jogo": "Áustria x Jordânia",          "local": "San Francisco",    "brasil": False},
    {"data": "17/06", "hora": "14h00", "jogo": "Portugal x RD Congo",         "local": "Houston",          "brasil": False},
    {"data": "17/06", "hora": "17h00", "jogo": "Inglaterra x Croácia",        "local": "Dallas",           "brasil": False},
    {"data": "17/06", "hora": "20h00", "jogo": "Gana x Panamá",               "local": "Toronto",          "brasil": False},
    {"data": "17/06", "hora": "23h00", "jogo": "Uzbequistão x Colômbia",      "local": "Cidade do México", "brasil": False},
    {"data": "18/06", "hora": "13h00", "jogo": "Tchéquia x África do Sul",    "local": "Atlanta",          "brasil": False},
    {"data": "18/06", "hora": "16h00", "jogo": "Suíça x Bósnia",              "local": "Los Angeles",      "brasil": False},
    {"data": "18/06", "hora": "19h00", "jogo": "Canadá x Catar",              "local": "Vancouver",        "brasil": False},
    {"data": "18/06", "hora": "22h00", "jogo": "México x Coreia do Sul",      "local": "Guadalajara",      "brasil": False},
    {"data": "19/06", "hora": "16h00", "jogo": "Estados Unidos x Austrália",  "local": "Seattle",          "brasil": False},
    {"data": "19/06", "hora": "19h00", "jogo": "Escócia x Marrocos",          "local": "Boston",           "brasil": False},
    {"data": "19/06", "hora": "21h30", "jogo": "Brasil x Haiti",              "local": "Filadélfia",       "brasil": True},
    {"data": "20/06", "hora": "00h00", "jogo": "Turquia x Paraguai",          "local": "San Francisco",    "brasil": False},
    {"data": "20/06", "hora": "14h00", "jogo": "Países Baixos x Suécia",      "local": "Houston",          "brasil": False},
    {"data": "20/06", "hora": "17h00", "jogo": "Alemanha x Costa do Marfim",  "local": "Toronto",          "brasil": False},
    {"data": "20/06", "hora": "21h00", "jogo": "Equador x Curaçao",           "local": "Kansas City",      "brasil": False},
    {"data": "21/06", "hora": "01h00", "jogo": "Tunísia x Japão",             "local": "Monterrey",        "brasil": False},
    {"data": "21/06", "hora": "13h00", "jogo": "Espanha x Arábia Saudita",    "local": "Atlanta",          "brasil": False},
    {"data": "21/06", "hora": "16h00", "jogo": "Bélgica x Irã",               "local": "Los Angeles",      "brasil": False},
    {"data": "21/06", "hora": "19h00", "jogo": "Uruguai x Cabo Verde",        "local": "Miami",            "brasil": False},
    {"data": "21/06", "hora": "22h00", "jogo": "Nova Zelândia x Egito",       "local": "Vancouver",        "brasil": False},
    {"data": "22/06", "hora": "14h00", "jogo": "Argentina x Áustria",         "local": "Dallas",           "brasil": False},
    {"data": "22/06", "hora": "18h00", "jogo": "França x Iraque",             "local": "Filadélfia",       "brasil": False},
    {"data": "22/06", "hora": "21h00", "jogo": "Noruega x Senegal",           "local": "Nova York/NJ",     "brasil": False},
    {"data": "23/06", "hora": "00h00", "jogo": "Jordânia x Argélia",          "local": "San Francisco",    "brasil": False},
    {"data": "23/06", "hora": "14h00", "jogo": "Portugal x Uzbequistão",      "local": "Houston",          "brasil": False},
    {"data": "23/06", "hora": "17h00", "jogo": "Inglaterra x Gana",           "local": "Boston",           "brasil": False},
    {"data": "23/06", "hora": "20h00", "jogo": "Panamá x Croácia",            "local": "Toronto",          "brasil": False},
    {"data": "23/06", "hora": "23h00", "jogo": "Colômbia x RD Congo",         "local": "Guadalajara",      "brasil": False},
    {"data": "24/06", "hora": "16h00", "jogo": "Suíça x Canadá",              "local": "Vancouver",        "brasil": False},
    {"data": "24/06", "hora": "16h00", "jogo": "Bósnia x Catar",              "local": "Seattle",          "brasil": False},
    {"data": "24/06", "hora": "19h00", "jogo": "Escócia x Brasil",            "local": "Miami",            "brasil": True},
    {"data": "24/06", "hora": "19h00", "jogo": "Marrocos x Haiti",            "local": "Atlanta",          "brasil": False},
    {"data": "24/06", "hora": "22h00", "jogo": "Tchéquia x México",           "local": "Cidade do México", "brasil": False},
    {"data": "24/06", "hora": "22h00", "jogo": "África do Sul x Coreia",      "local": "Monterrey",        "brasil": False},
    {"data": "25/06", "hora": "17h00", "jogo": "Equador x Alemanha",          "local": "Nova York/NJ",     "brasil": False},
    {"data": "25/06", "hora": "17h00", "jogo": "Curaçao x Costa do Marfim",   "local": "Filadélfia",       "brasil": False},
    {"data": "25/06", "hora": "20h00", "jogo": "Japão x Suécia",              "local": "Dallas",           "brasil": False},
    {"data": "25/06", "hora": "20h00", "jogo": "Tunísia x Países Baixos",     "local": "Kansas City",      "brasil": False},
    {"data": "25/06", "hora": "23h00", "jogo": "Turquia x Estados Unidos",    "local": "Los Angeles",      "brasil": False},
    {"data": "25/06", "hora": "23h00", "jogo": "Paraguai x Austrália",        "local": "San Francisco",    "brasil": False},
    {"data": "26/06", "hora": "16h00", "jogo": "Noruega x França",            "local": "Boston",           "brasil": False},
    {"data": "26/06", "hora": "16h00", "jogo": "Senegal x Iraque",            "local": "Toronto",          "brasil": False},
    {"data": "26/06", "hora": "21h00", "jogo": "Cabo Verde x Arábia Saudita", "local": "Houston",          "brasil": False},
    {"data": "26/06", "hora": "21h00", "jogo": "Uruguai x Espanha",           "local": "Guadalajara",      "brasil": False},
    {"data": "27/06", "hora": "00h00", "jogo": "Egito x Irã",                 "local": "Seattle",          "brasil": False},
    {"data": "27/06", "hora": "00h00", "jogo": "Nova Zelândia x Bélgica",     "local": "Vancouver",        "brasil": False},
    {"data": "27/06", "hora": "18h00", "jogo": "Panamá x Inglaterra",         "local": "Nova York/NJ",     "brasil": False},
    {"data": "27/06", "hora": "18h00", "jogo": "Croácia x Gana",              "local": "Filadélfia",       "brasil": False},
    {"data": "27/06", "hora": "20h30", "jogo": "Colômbia x Portugal",         "local": "Miami",            "brasil": False},
    {"data": "27/06", "hora": "20h30", "jogo": "RD Congo x Uzbequistão",      "local": "Atlanta",          "brasil": False},
    {"data": "27/06", "hora": "23h00", "jogo": "Argélia x Áustria",           "local": "Kansas City",      "brasil": False},
    {"data": "27/06", "hora": "23h00", "jogo": "Jordânia x Argentina",        "local": "Dallas",           "brasil": False},
]

# ==============================================================================
# BANCO DE DADOS — JSONBin.io
# ==============================================================================
def _jsonbin_headers():
    key = st.secrets.get("JSONBIN_KEY", "")
    return {"Content-Type": "application/json", "X-Master-Key": key}

def _jsonbin_url():
    bin_id = st.secrets.get("JSONBIN_ID", "")
    return f"https://api.jsonbin.io/v3/b/{bin_id}"

def _banco_padrao():
    banco = {}
    todos_ids_mm     = {c["id"]: "" for c in MATA_MATA_CONFRONTOS}
    todos_placares_mm = {c["id"]: [0, 0] for c in MATA_MATA_CONFRONTOS}
    for amigo in AMIGOS:
        banco[amigo] = {
            "travado":              False,
            "classificacao":        {g: list(t) for g, t in GRUPOS_CONFIG.items()},
            "placar_brasil":        [0, 0, 0, 0, 0, 0],
            "vencedores_mata_mata": dict(todos_ids_mm),
            "palpites_placar_mm":   dict(todos_placares_mm),
            "mm_oitavas_travadas":  False,
            "mm_quartas_travadas":  False,
            "mm_semis_travadas":    False,
            "mm_final_travada":     False,
        }
    return banco

def carregar_banco():
    banco_seguro = _banco_padrao()
    try:
        bin_id  = st.secrets.get("JSONBIN_ID", "")
        api_key = st.secrets.get("JSONBIN_KEY", "")
        if not bin_id or not api_key:
            return banco_seguro

        resp = requests.get(_jsonbin_url(), headers=_jsonbin_headers(), timeout=6)

        if resp.status_code == 200:
            dados = resp.json().get("record", {})

            if not dados or not isinstance(dados, dict) or not any(a in dados for a in AMIGOS):
                requests.put(_jsonbin_url(), json=banco_seguro, headers=_jsonbin_headers(), timeout=8)
                return banco_seguro

            todos_ids_mm     = {c["id"]: "" for c in MATA_MATA_CONFRONTOS}
            todos_placares_mm = {c["id"]: [0, 0] for c in MATA_MATA_CONFRONTOS}

            for amigo in AMIGOS:
                if amigo in dados:
                    d = dados[amigo]
                    banco_seguro[amigo]["travado"]       = bool(d.get("travado", False))
                    banco_seguro[amigo]["classificacao"] = d.get("classificacao", banco_seguro[amigo]["classificacao"])
                    banco_seguro[amigo]["placar_brasil"] = d.get("placar_brasil", banco_seguro[amigo]["placar_brasil"])
                    mm_salvo = d.get("vencedores_mata_mata", {})
                    banco_seguro[amigo]["vencedores_mata_mata"] = {**todos_ids_mm, **mm_salvo}
                    pp_salvo = d.get("palpites_placar_mm", {})
                    banco_seguro[amigo]["palpites_placar_mm"] = {**todos_placares_mm, **pp_salvo}
                    banco_seguro[amigo]["mm_oitavas_travadas"] = bool(d.get("mm_oitavas_travadas", False))
                    banco_seguro[amigo]["mm_quartas_travadas"] = bool(d.get("mm_quartas_travadas", False))
                    banco_seguro[amigo]["mm_semis_travadas"]   = bool(d.get("mm_semis_travadas", False))
                    banco_seguro[amigo]["mm_final_travada"]    = bool(d.get("mm_final_travada", False))

            return banco_seguro

        if resp.status_code in (401, 403):
            st.warning("⚠️ JSONBin: chave de API inválida. Rodando em modo local.")
        elif resp.status_code == 404:
            st.warning("⚠️ JSONBin: bin não encontrado.")

    except requests.exceptions.Timeout:
        st.warning("⚠️ JSONBin sem resposta (timeout). Rodando com dados locais.")
    except Exception:
        pass

    return banco_seguro

def salvar_banco(banco_completo):
    """
    Grava o banco completo no JSONBin via PUT.
    PROTEÇÃO: preserva palpites de usuários travados no banco remoto.
    """
    try:
        bin_id  = st.secrets.get("JSONBIN_ID", "")
        api_key = st.secrets.get("JSONBIN_KEY", "")
        if not bin_id or not api_key:
            st.session_state.banco = banco_completo
            return True

        # Busca o banco remoto atual para proteção
        resp_atual = requests.get(_jsonbin_url(), headers=_jsonbin_headers(), timeout=6)
        if resp_atual.status_code == 200:
            banco_remoto = resp_atual.json().get("record", {})
            for amigo in AMIGOS:
                if banco_remoto.get(amigo, {}).get("travado"):
                    banco_completo[amigo]["classificacao"] = banco_remoto[amigo]["classificacao"]
                    banco_completo[amigo]["placar_brasil"] = banco_remoto[amigo]["placar_brasil"]
                    banco_completo[amigo]["travado"]       = True

        resp = requests.put(_jsonbin_url(), json=banco_completo, headers=_jsonbin_headers(), timeout=8)
        if resp.status_code == 200:
            st.session_state.banco = banco_completo
            return True
        else:
            st.error(f"Erro ao salvar (HTTP {resp.status_code}): {resp.text[:200]}")
    except requests.exceptions.Timeout:
        st.error("Timeout ao salvar na nuvem. Tente novamente.")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
    return False

# ==============================================================================
# INICIALIZAÇÃO DO SESSION_STATE
# ==============================================================================
if "banco" not in st.session_state:
    st.session_state.banco = carregar_banco()

padrao = _banco_padrao()
for amigo in AMIGOS:
    if amigo not in st.session_state.banco:
        st.session_state.banco[amigo] = padrao[amigo]
    # Campos novos em bancos antigos
    for campo, val in padrao[amigo].items():
        if campo not in st.session_state.banco[amigo]:
            st.session_state.banco[amigo][campo] = val

# ==============================================================================
# AUTENTICAÇÃO POR PIN
# ==============================================================================
PINS = {
    "Fefo":  st.secrets.get("PIN_FEFO",  "1111"),
    "Vini":  st.secrets.get("PIN_VINI",  "2222"),
    "Nico":  st.secrets.get("PIN_NICO",  "3333"),
    "Bruno": st.secrets.get("PIN_BRUNO", "4444"),
    "Renan": st.secrets.get("PIN_RENAN", "5555"),
    "Juan":  st.secrets.get("PIN_JUAN",  "6666"),
}

if "usuario_autenticado" not in st.session_state:
    st.session_state.usuario_autenticado = None
if "tentativas_pin" not in st.session_state:
    st.session_state.tentativas_pin = 0

# ==============================================================================
# RESULTADOS REAIS DA API
# ==============================================================================
TRADUCAO = {
    "Brazil": "Brasil", "Haiti": "Haiti", "Morocco": "Marrocos", "Scotland": "Escócia",
    "Mexico": "México", "South Africa": "África do Sul",
    "Korea Republic": "Coreia do Sul", "Czech Republic": "Tchéquia", "Czechia": "Tchéquia",
    "Bosnia and Herzegovina": "Bósnia e Herzegovina", "Bosnia-Herzegovina": "Bósnia e Herzegovina",
    "Canada": "Canadá", "Qatar": "Catar", "Switzerland": "Suíça",
    "Australia": "Austrália", "Paraguay": "Paraguai", "Turkey": "Turquia",
    "USA": "Estados Unidos", "United States": "Estados Unidos",
    "Curaçao": "Curaçao", "Curaþao": "Curaçao",
    "Ecuador": "Equador", "Germany": "Alemanha",
    "Ivory Coast": "Costa do Marfim", "Cote d'Ivoire": "Costa do Marfim",
    "Japan": "Japão", "Netherlands": "Países Baixos", "Sweden": "Suécia", "Tunisia": "Tunísia",
    "Belgium": "Bélgica", "Egypt": "Egito", "Iran": "Irã", "New Zealand": "Nova Zelândia",
    "Cape Verde": "Cabo Verde", "Cape Verde Islands": "Cabo Verde",
    "Saudi Arabia": "Arábia Saudita", "Spain": "Espanha", "Uruguay": "Uruguai",
    "South Korea": "Coreia do Sul",
    "France": "França", "Iraq": "Iraque", "Norway": "Noruega", "Senegal": "Senegal",
    "Algeria": "Argélia", "Argentina": "Argentina", "Austria": "Áustria", "Jordan": "Jordânia",
    "Colombia": "Colômbia", "DR Congo": "RD Congo", "Congo DR": "RD Congo",
    "Portugal": "Portugal", "Uzbekistan": "Uzbequistão",
    "Croatia": "Croácia", "England": "Inglaterra", "Ghana": "Gana", "Panama": "Panamá",
}

ALIASES_TIMES = {
    "Coreia": "República da Coreia",
    "Coreia do Sul": "República da Coreia",
    "República da Coreia": "República da Coreia",
    "Bósnia": "Bósnia e Herzegovina",
    "Bósnia e Herzegovina": "Bósnia e Herzegovina",
    "Bosnia": "Bósnia e Herzegovina",
    "Bosnia and Herzegovina": "Bósnia e Herzegovina",
    "Bosnia-Herzegovina": "Bósnia e Herzegovina",
    "USA": "Estados Unidos",
    "United States": "Estados Unidos",
    "United States of America": "Estados Unidos",
    "Czech Republic": "Tchéquia",
    "Czechia": "Tchéquia",
}

# Resultados já conhecidos (preenchimento manual como fallback de API)
RESULTADOS_MANUAIS = {
    "México x África do Sul":   {"placar_c": 2, "placar_f": 0},
    "Tchéquia x Coreia do Sul": {"placar_c": 1, "placar_f": 2},
    "Canadá x Bósnia":          {"placar_c": 1, "placar_f": 1},
    "Estados Unidos x Paraguai":{"placar_c": 4, "placar_f": 1},
    "Catar x Suíça":            {"placar_c": 1, "placar_f": 1},
    "Brasil x Marrocos":        {"placar_c": 1, "placar_f": 1},
}

def _resultados_manuais():
    resultados = dict(RESULTADOS_MANUAIS)
    try:
        raw = st.secrets.get("RESULTADOS_MANUAIS_JSON", "")
        if raw:
            resultados.update(json.loads(raw))
    except Exception:
        pass
    return resultados

def _resultados_manuais_mm():
    """Resultados do mata-mata via secrets. Formato: MM_M1, MM_Q1 etc."""
    try:
        raw = st.secrets.get("RESULTADOS_MM_JSON", "")
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return {}

def _agora_brt():
    return datetime.now(BRT)

def _normalizar_time(nome):
    nome = (nome or "").strip()
    traduzido = TRADUCAO.get(nome, nome)
    return ALIASES_TIMES.get(traduzido, traduzido)

def _partes_jogo(nome_jogo):
    partes = nome_jogo.replace(" x ", "|").split("|")
    if len(partes) < 2:
        return "", ""
    return _normalizar_time(partes[0]), _normalizar_time(partes[1])

def _datetime_jogo_brt(data_str, hora_str):
    h_num = hora_str.replace("h", ":").rstrip(":")
    if len(h_num) == 2:
        h_num = f"{h_num}:00"
    return datetime.strptime(f"2026/{data_str} {h_num}", "%Y/%d/%m %H:%M").replace(tzinfo=BRT)

def _status_por_data_hora(data_str, hora_str):
    try:
        delta = (_agora_brt() - _datetime_jogo_brt(data_str, hora_str)).total_seconds() / 60
        if delta > DURACAO_JOGO_MIN:
            return "finalizado"
        if 0 <= delta <= DURACAO_JOGO_MIN:
            return "aovivo"
        return "previsto"
    except Exception:
        return "previsto"

def _status_api_para_padrao(status):
    status = (status or "").upper()
    if status in ("FINISHED", "FT", "ENDED", "AET", "PEN"):
        return "FINISHED"
    if status in ("IN_PLAY", "LIVE", "PAUSED", "1H", "2H", "HT"):
        return "IN_PLAY"
    return "SCHEDULED"

def _tem_placar(jogo):
    return jogo.get("placar_c") is not None and jogo.get("placar_f") is not None

def _formatar_placar(jogo):
    casa, fora = _partes_jogo(jogo["jogo"])
    if _tem_placar(jogo):
        return f"{casa} {jogo['placar_c']} x {jogo['placar_f']} {fora}"
    return f"{casa} x {fora}"

def _jogos_mesmas_selecoes(jogo_a, jogo_b):
    return set(_partes_jogo(jogo_a)) == set(_partes_jogo(jogo_b))

def _calendario_para_jogo(nome_jogo):
    for jogo in CALENDARIO_FIXO:
        if _jogos_mesmas_selecoes(nome_jogo, jogo["jogo"]):
            return jogo
    return None

def _aplicar_overrides_calendario(jogos_reais):
    resultados_manuais = _resultados_manuais()
    jogos = []
    for jogo in jogos_reais:
        item = dict(jogo)
        item.setdefault("fonte_resultado", item.get("fonte_resultado", "API"))
        calendario = _calendario_para_jogo(item["jogo"])
        if calendario:
            status_cal = _status_por_data_hora(calendario["data"], calendario["hora"])
            if status_cal == "finalizado" and item.get("status") == "SCHEDULED":
                item["status"] = "FINISHED"
                item["fonte_resultado"] = "calendário"
            elif status_cal == "aovivo" and item.get("status") == "SCHEDULED":
                item["status"] = "IN_PLAY"
                item["fonte_resultado"] = "calendário"

        manual = resultados_manuais.get(item["jogo"])
        origem_manual = item["jogo"]
        if not manual and calendario:
            origem_manual = calendario["jogo"]
            manual = resultados_manuais.get(origem_manual)

        if manual:
            gc = manual.get("placar_c")
            gf = manual.get("placar_f")
            if origem_manual != item["jogo"]:
                item_casa, item_fora = _partes_jogo(item["jogo"])
                origem_casa, origem_fora = _partes_jogo(origem_manual)
                if item_casa == origem_fora and item_fora == origem_casa:
                    gc, gf = gf, gc
            item["placar_c"] = gc
            item["placar_f"] = gf
            item["fonte_resultado"] = "manual"
            if gc is not None and gf is not None:
                item["status"] = "FINISHED"
        jogos.append(item)
    return jogos

def _jogos_do_calendario_fixo():
    jogos = []
    resultados_manuais = _resultados_manuais()
    for jogo in CALENDARIO_FIXO:
        status_cal = _status_por_data_hora(jogo["data"], jogo["hora"])
        placar_manual = resultados_manuais.get(jogo["jogo"], {})
        jogos.append({
            "jogo":     jogo["jogo"],
            "placar_c": placar_manual.get("placar_c"),
            "placar_f": placar_manual.get("placar_f"),
            "status":   "FINISHED" if status_cal == "finalizado" else ("IN_PLAY" if status_cal == "aovivo" else "SCHEDULED"),
            "fonte_resultado": "manual" if placar_manual else "calendário",
        })
    return jogos

def _buscar_jogo_real(nome_jogo):
    for jogo in api_data.get("jogos_reais", []):
        if _jogos_mesmas_selecoes(jogo["jogo"], nome_jogo):
            return jogo
    return None

def _jogos_do_grupo(nome_grupo, apenas_com_placar=False):
    jogos = []
    times_norm = {_normalizar_time(t) for t in GRUPOS_CONFIG[nome_grupo]}
    for jogo in api_data.get("jogos_reais", []):
        t_c, t_f = _partes_jogo(jogo["jogo"])
        if t_c in times_norm and t_f in times_norm:
            if apenas_com_placar and not (jogo.get("status") == "FINISHED" and _tem_placar(jogo)):
                continue
            jogos.append(jogo)
    return jogos

def _grupo_do_jogo(nome_jogo):
    t_c, t_f = _partes_jogo(nome_jogo)
    for nome_grupo, times in GRUPOS_CONFIG.items():
        times_norm = {_normalizar_time(t) for t in times}
        if t_c in times_norm or t_f in times_norm:
            return nome_grupo
    return None

def _classificacao_por_jogos(jogos_reais):
    tabelas = {g: {time: {"pts": 0, "sg": 0, "gp": 0, "idx": i} for i, time in enumerate(times)}
               for g, times in GRUPOS_CONFIG.items()}

    for jogo in jogos_reais:
        if jogo.get("status") != "FINISHED":
            continue
        gc = jogo.get("placar_c")
        gf = jogo.get("placar_f")
        if gc is None or gf is None:
            continue
        grupo = _grupo_do_jogo(jogo["jogo"])
        if not grupo:
            continue
        casa, fora = _partes_jogo(jogo["jogo"])
        casa_real = next((t for t in tabelas[grupo] if _normalizar_time(t) == casa), None)
        fora_real = next((t for t in tabelas[grupo] if _normalizar_time(t) == fora), None)
        if not casa_real or not fora_real:
            continue

        tabelas[grupo][casa_real]["gp"] += gc
        tabelas[grupo][casa_real]["sg"] += gc - gf
        tabelas[grupo][fora_real]["gp"] += gf
        tabelas[grupo][fora_real]["sg"] += gf - gc
        if gc > gf:
            tabelas[grupo][casa_real]["pts"] += 3
        elif gc < gf:
            tabelas[grupo][fora_real]["pts"] += 3
        else:
            tabelas[grupo][casa_real]["pts"] += 1
            tabelas[grupo][fora_real]["pts"] += 1

    classificacao = {}
    for grupo, times in tabelas.items():
        classificacao[grupo] = sorted(
            times,
            key=lambda t: (-tabelas[grupo][t]["pts"], -tabelas[grupo][t]["sg"],
                           -tabelas[grupo][t]["gp"], tabelas[grupo][t]["idx"])
        )
    return classificacao

def _montar_resultado(jogos_reais, fonte, classificacao_real=None):
    for jogo in jogos_reais:
        jogo.setdefault("fonte_resultado", fonte)
    jogos_reais = _aplicar_overrides_calendario(jogos_reais)

    gols_brasil = [None] * 6
    idx_br = 0
    for j in jogos_reais:
        if j["status"] == "FINISHED" and idx_br < 3:
            gc, gf = j["placar_c"], j["placar_f"]
            if gc is None or gf is None:
                continue
            nome = j["jogo"]
            if nome.startswith("Brasil"):
                gols_brasil[idx_br * 2]     = gc
                gols_brasil[idx_br * 2 + 1] = gf
                idx_br += 1
            elif " x Brasil" in nome or nome.endswith("Brasil"):
                gols_brasil[idx_br * 2]     = gf
                gols_brasil[idx_br * 2 + 1] = gc
                idx_br += 1

    classificacao_calculada = _classificacao_por_jogos(jogos_reais)
    classificacao_final = {}
    for grupo in GRUPOS_CONFIG:
        if classificacao_real and grupo in classificacao_real and len(classificacao_real[grupo]) == 4:
            classificacao_final[grupo] = classificacao_real[grupo]
        elif grupo in classificacao_calculada:
            classificacao_final[grupo] = classificacao_calculada[grupo]
        else:
            classificacao_final[grupo] = list(GRUPOS_CONFIG[grupo])

    return {
        "fonte":              fonte,
        "classificacao_real": classificacao_final,
        "jogos_reais":        jogos_reais,
        "gols_brasil":        gols_brasil,
        "jogos_mata_mata":    [],
    }

def _classificacao_football_data(token):
    try:
        url = "https://api.football-data.org/v4/competitions/WC/standings?season=2026"
        r = requests.get(url, headers={"X-Auth-Token": token}, timeout=6)
        if r.status_code != 200:
            return {}
        retorno = {}
        for standing in r.json().get("standings", []):
            grupo_api = standing.get("group", "")
            if not grupo_api:
                continue
            letra = grupo_api.split("_")[-1].upper()
            nome_grupo = f"Grupo {letra}"
            if nome_grupo not in GRUPOS_CONFIG:
                continue
            ordem = []
            for linha in standing.get("table", []):
                nome_time = linha.get("team", {}).get("name", "")
                nome_norm = _normalizar_time(nome_time)
                time_local = next(
                    (t for t in GRUPOS_CONFIG[nome_grupo] if _normalizar_time(t) == nome_norm),
                    None
                )
                if time_local:
                    ordem.append(time_local)
            if ordem:
                faltando = [t for t in GRUPOS_CONFIG[nome_grupo] if t not in ordem]
                retorno[nome_grupo] = ordem + faltando
        return retorno
    except Exception as e:
        st.warning(f"⚠️ Erro ao buscar classificação da API: {e}")
        return {}

@st.cache_data(ttl=120)
def obter_resultados():
    padrao = {
        "fonte":              "calendário fixo",
        "classificacao_real": {g: list(t) for g, t in GRUPOS_CONFIG.items()},
        "jogos_reais":        [],
        "gols_brasil":        [None] * 6,
        "jogos_mata_mata":    [],
    }

    # ── API 1: football-data.org ──────────────────────────────────────────────
    try:
        token = st.secrets.get("FOOTBALL_DATA_TOKEN", "52974ada524e459ea4cf52a9dcc19861")
        if token:
            url = "https://api.football-data.org/v4/competitions/WC/matches"
            r = requests.get(url, headers={"X-Auth-Token": token}, timeout=6)
            if r.status_code != 200:
                st.warning(f"⚠️ Football-Data retornou HTTP {r.status_code}. Usando dados manuais.")
            else:
                matches = r.json().get("matches", [])
                if not matches:
                    st.warning("⚠️ Football-Data retornou sem jogos.")
                else:
                    jogos_grupos = []
                    jogos_mm     = []
                    STAGES_MM = {"ROUND_OF_16", "QUARTER_FINALS", "SEMI_FINALS", "THIRD_PLACE", "FINAL"}
                    for m in matches:
                        t_c   = _normalizar_time(m["homeTeam"]["name"])
                        t_f   = _normalizar_time(m["awayTeam"]["name"])
                        score = m.get("score") or {}
                        ft    = score.get("fullTime") or {}
                        gc    = ft.get("home", ft.get("homeTeam"))
                        gf    = ft.get("away", ft.get("awayTeam"))
                        status = m.get("status", "SCHEDULED")
                        stage  = m.get("stage", "")
                        item = {
                            "jogo":     f"{t_c} x {t_f}",
                            "placar_c": gc,
                            "placar_f": gf,
                            "status":   _status_api_para_padrao(status),
                            "stage":    stage,
                        }
                        if stage in STAGES_MM:
                            jogos_mm.append(item)
                        else:
                            jogos_grupos.append(item)

                    st.success(f"✅ Football-Data: {len(jogos_grupos)} jogos grupos, {len(jogos_mm)} mata-mata")
                    classificacao_api = _classificacao_football_data(token)
                    resultado = _montar_resultado(jogos_grupos, "football-data.org", classificacao_api)
                    resultado["jogos_mata_mata"] = jogos_mm
                    return resultado
    except Exception as e:
        st.error(f"❌ Erro football-data: {e}")

    # ── API 2: Zafronix Sports API ────────────────────────────────────────────
    try:
        token_zafronix = st.secrets.get("ZAFRONIX_KEY", "zwc_free_85be12c14621f2117b7dae7f")
        url = "https://api.zafronix.com/fifa/worldcup/v1/tournaments/2026/fixtures"
        r = requests.get(url, headers={"X-API-Key": token_zafronix}, timeout=5)
        if r.status_code == 200:
            fixtures = r.json().get("fixtures", [])
            if fixtures:
                jogos_grupos = []
                jogos_mm     = []
                for m in fixtures:
                    t_c   = _normalizar_time(m.get("home_team", ""))
                    t_f   = _normalizar_time(m.get("away_team", ""))
                    gc    = m.get("home_score")
                    gf    = m.get("away_score")
                    st_   = m.get("status", "SCHEDULED")
                    stage = str(m.get("stage", m.get("round", ""))).upper()
                    item  = {
                        "jogo":     f"{t_c} x {t_f}",
                        "placar_c": gc,
                        "placar_f": gf,
                        "status":   _status_api_para_padrao(st_),
                    }
                    if any(k in stage for k in ["ROUND_OF_16", "QUARTER", "SEMI", "FINAL", "THIRD"]):
                        jogos_mm.append(item)
                    else:
                        jogos_grupos.append(item)
                resultado = _montar_resultado(jogos_grupos, "Zafronix Sports API")
                resultado["jogos_mata_mata"] = jogos_mm
                return resultado
    except Exception:
        pass

    # ── API 3: Sportmonks ────────────────────────────────────────────────────
    try:
        token_sm = st.secrets.get("SPORTMONKS_TOKEN", "")
        if token_sm:
            url = f"https://api.sportmonks.com/v3/football/fixtures?api_token={token_sm}&include=participants,scores"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                fixtures = r.json().get("data", [])
                if fixtures:
                    jogos = []
                    for m in fixtures:
                        participants = m.get("participants", [])
                        if len(participants) < 2:
                            continue
                        t_c = _normalizar_time(participants[0].get("name", ""))
                        t_f = _normalizar_time(participants[1].get("name", ""))
                        scores = m.get("scores", {})
                        gc  = scores.get("localteam_score")
                        gf  = scores.get("visitorteam_score")
                        st_ = m.get("state", {})
                        state_name = st_.get("name", "") if isinstance(st_, dict) else str(st_)
                        jogos.append({
                            "jogo":     f"{t_c} x {t_f}",
                            "placar_c": gc,
                            "placar_f": gf,
                            "status":   _status_api_para_padrao(state_name),
                        })
                    if jogos:
                        resultado = _montar_resultado(jogos, "Sportmonks")
                        return resultado
    except Exception:
        pass

    jogos_fallback = _jogos_do_calendario_fixo()
    return _montar_resultado(jogos_fallback, "calendário fixo")

api_data = obter_resultados()

# ==============================================================================
# HELPERS — classificação e mata-mata
# ==============================================================================
def _status_jogo(data_str, hora_str):
    return _status_por_data_hora(data_str, hora_str)

def _countdown_brasil():
    agora = _agora_brt()
    alvo  = PROXIMO_JOGO_BRASIL["data_hora"]
    delta = alvo - agora
    if delta.total_seconds() <= 0:
        return None
    horas   = int(delta.total_seconds() // 3600)
    minutos = int((delta.total_seconds() % 3600) // 60)
    dias    = horas // 24
    horas_r = horas % 24
    if dias > 0:
        return f"{dias}d {horas_r:02d}h {minutos:02d}min", PROXIMO_JOGO_BRASIL["nome"]
    return f"{horas:02d}h {minutos:02d}min", PROXIMO_JOGO_BRASIL["nome"]

def _grupos_com_resultado():
    finalizados = set()
    for nome_grupo, times in GRUPOS_CONFIG.items():
        for jogo in api_data.get("jogos_reais", []):
            if jogo.get("status") != "FINISHED" or not _tem_placar(jogo):
                continue
            t_c, t_f = _partes_jogo(jogo["jogo"])
            times_norm = {_normalizar_time(t) for t in times}
            if t_c in times_norm or t_f in times_norm:
                finalizados.add(nome_grupo)
                break
    return finalizados

def _classificacao_real():
    """Retorna a classificação real disponível (da API ou calculada)."""
    return api_data.get("classificacao_real", {g: list(t) for g, t in GRUPOS_CONFIG.items()})

def _nome_real_por_pos(grupo_letra, posicao):
    """
    Resolve '1º do Grupo E' para o nome real da seleção.
    posicao: 1-based (1=primeiro, 2=segundo…)
    Retorna None se classificação ainda não disponível.
    """
    nome_grupo = f"Grupo {grupo_letra}"
    classificacao = _classificacao_real()
    times = classificacao.get(nome_grupo, [])
    idx = posicao - 1
    if idx < len(times) and times[idx]:
        return times[idx]
    return None

def _resolver_times_oitava(conf_def, labels):
    """
    Tenta resolver os nomes reais de uma oitava.
    conf_def: {"id":..., "pos1": (letra, pos), "pos2": (letra, pos)}
    labels:   {"id":..., "t1": "1º Grupo E", "t2": "3º colocado"}
    Retorna (t1_display, t2_display) com nomes reais se disponíveis.
    """
    def _resolver(pos_tuple, label_fallback):
        letra, pos = pos_tuple
        if letra == "?" or pos == 0:
            return label_fallback  # 3º colocado ainda indefinido
        nome = _nome_real_por_pos(letra, pos)
        return nome if nome else label_fallback

    t1 = _resolver(conf_def["pos1"], labels["t1"])
    t2 = _resolver(conf_def["pos2"], labels["t2"])
    return t1, t2

def _buscar_resultado_mm_api(t1, t2):
    """Busca resultado de um jogo do mata-mata pelos nomes dos times."""
    t1n = _normalizar_time(t1)
    t2n = _normalizar_time(t2)
    for jogo in api_data.get("jogos_mata_mata", []):
        jc, jf = _partes_jogo(jogo["jogo"])
        if (jc == t1n and jf == t2n) or (jc == t2n and jf == t1n):
            return jogo
    return None

def _resultado_mm(conf_id, t1, t2):
    """
    Retorna dict com placar e vencedor de um jogo do mata-mata.
    Prioridade: resultado manual (secrets) > API > None
    """
    # 1. Manual via secrets (chave MM_M1, MM_Q1…)
    manuais = _resultados_manuais_mm()
    manual = manuais.get(f"MM_{conf_id}")
    if manual:
        gc = manual.get("placar_c")
        gf = manual.get("placar_f")
        tc = manual.get("time_casa", t1)
        tf = manual.get("time_fora", t2)
        venc = manual.get("vencedor", "")
        if not venc and gc is not None and gf is not None and gc != gf:
            venc = tc if gc > gf else tf
        return {"placar_c": gc, "placar_f": gf, "time_casa": tc, "time_fora": tf,
                "vencedor": venc, "fonte": "manual"}
    # 2. API
    if t1 and t2 and "colocado" not in t1 and "Venc." not in t1:
        jogo_api = _buscar_resultado_mm_api(t1, t2)
        if jogo_api and jogo_api.get("status") == "FINISHED" and _tem_placar(jogo_api):
            gc = jogo_api["placar_c"]
            gf = jogo_api["placar_f"]
            jc, jf = _partes_jogo(jogo_api["jogo"])
            # Garante correspondência casa/fora com t1/t2
            t1n = _normalizar_time(t1)
            if jc == t1n:
                gc_t1, gf_t2 = gc, gf
            else:
                gc_t1, gf_t2 = gf, gc
            venc = t1 if gc_t1 > gf_t2 else (t2 if gf_t2 > gc_t1 else "")
            return {"placar_c": gc_t1, "placar_f": gf_t2,
                    "time_casa": t1, "time_fora": t2,
                    "vencedor": venc, "fonte": "API"}
    return None

def _calcular_pontuacao(amigo):
    user  = st.session_state.banco[amigo]
    real  = api_data
    total = 0
    dets  = []

    if not user["travado"]:
        return 0, []

    grupos_ativos = _grupos_com_resultado()

    # ── Grupos ──
    for g in GRUPOS_CONFIG:
        if g not in grupos_ativos:
            continue
        for pos_idx, pos_label in [(0, "1º"), (1, "2º")]:
            palpite = user["classificacao"][g][pos_idx]
            real_t  = real["classificacao_real"][g][pos_idx]
            acertou = _normalizar_time(palpite) == _normalizar_time(real_t)
            pts     = 2 if acertou else 0
            total  += pts
            dets.append({"cat": g,
                         "texto": f"{pos_label} colocado: palpite {palpite}; atual {real_t}",
                         "pts": pts, "status": "ok" if acertou else "err"})

    # ── Jogos do Brasil ──
    for i in range(3):
        b    = i * 2
        p_br = user["placar_brasil"][b]
        p_ad = user["placar_brasil"][b + 1]
        r_br = real["gols_brasil"][b]
        r_ad = real["gols_brasil"][b + 1]
        nj   = JOGOS_BRASIL[i]["jogo"]
        if r_br is None or r_ad is None:
            dets.append({"cat": "Jogos do Brasil",
                         "texto": f"{nj}: palpite {p_br}x{p_ad}; aguardando resultado",
                         "pts": 0, "status": "wait"})
            continue
        if p_br == r_br and p_ad == r_ad:
            pts, st_ = 5, "ok"
            texto = f"{nj}: placar exato! {p_br}x{p_ad}; real {r_br}x{r_ad}"
        elif ((p_br > p_ad and r_br > r_ad) or (p_br < p_ad and r_br < r_ad)
              or (p_br == p_ad and r_br == r_ad)):
            pts, st_ = 3, "ok"
            texto = f"{nj}: resultado correto; palpite {p_br}x{p_ad}; real {r_br}x{r_ad}"
        else:
            pts, st_ = 0, "err"
            texto = f"{nj}: palpite {p_br}x{p_ad}; real {r_br}x{r_ad}"
        total += pts
        dets.append({"cat": "Jogos do Brasil", "texto": texto, "pts": pts, "status": st_})

    # ── Mata-Mata ──
    fases_mm = [
        ("Oitavas de Final", "mm_oitavas_travadas",
         list(zip(MATA_MATA_OITAVAS_DEF, MATA_MATA_OITAVAS_LABELS))),
        ("Quartas de Final", "mm_quartas_travadas",
         [(None, c) for c in MATA_MATA_QUARTAS]),
        ("Semifinais",       "mm_semis_travadas",
         [(None, c) for c in MATA_MATA_SEMIS]),
        ("Final",            "mm_final_travada",
         [(None, c) for c in MATA_MATA_FINAL]),
    ]
    for nome_fase, campo_trava, pares in fases_mm:
        if not user.get(campo_trava):
            continue
        for conf_def, conf_label in pares:
            cid = conf_label["id"]
            # Resolve nomes reais
            if conf_def:
                t1_r, t2_r = _resolver_times_oitava(conf_def, conf_label)
            else:
                t1_r, t2_r = conf_label["t1"], conf_label["t2"]

            palpite_venc  = user["vencedores_mata_mata"].get(cid, "")
            palpite_pl    = user["palpites_placar_mm"].get(cid, [0, 0])
            resultado     = _resultado_mm(cid, t1_r, t2_r)

            if not palpite_venc:
                dets.append({"cat": f"Mata-Mata ({nome_fase})",
                             "texto": f"{t1_r} vs {t2_r}: sem palpite",
                             "pts": 0, "status": "err"})
                continue
            if not resultado:
                dets.append({"cat": f"Mata-Mata ({nome_fase})",
                             "texto": f"{t1_r} vs {t2_r}: aguardando resultado",
                             "pts": 0, "status": "wait"})
                continue

            real_venc = resultado.get("vencedor", "")
            real_gc   = resultado.get("placar_c")
            real_gf   = resultado.get("placar_f")
            p_gc = palpite_pl[0] if isinstance(palpite_pl, list) and len(palpite_pl) >= 2 else 0
            p_gf = palpite_pl[1] if isinstance(palpite_pl, list) and len(palpite_pl) >= 2 else 0

            acertou_placar = (real_gc is not None and real_gf is not None
                              and p_gc == real_gc and p_gf == real_gf)
            acertou_venc   = bool(palpite_venc and real_venc
                                  and _normalizar_time(palpite_venc) == _normalizar_time(real_venc))

            if acertou_placar:
                pts, st_ = 5, "ok"
                texto = f"{t1_r} vs {t2_r}: placar exato! {p_gc}x{p_gf}; venc. {real_venc}"
            elif acertou_venc:
                pts, st_ = 3, "ok"
                texto = f"{t1_r} vs {t2_r}: vencedor correto ({palpite_venc})"
            else:
                pts, st_ = 0, "err"
                texto = f"{t1_r} vs {t2_r}: palpite {palpite_venc}; real {real_venc or '?'}"

            total += pts
            dets.append({"cat": f"Mata-Mata ({nome_fase})",
                         "texto": texto, "pts": pts, "status": st_})

    return total, dets

# ==============================================================================
# CABEÇALHO
# ==============================================================================
st.markdown("# 🏆 Bolão do Bobão — Copa 2026")

resultado_countdown = _countdown_brasil()
if resultado_countdown:
    tempo_str, nome_jogo = resultado_countdown
    st.markdown(f"""
    <div class="countdown-box">
        <div class="countdown-label">⏱ Próximo jogo do Brasil</div>
        <div class="countdown-time">{tempo_str}</div>
        <div class="countdown-game">{nome_jogo} — trave seus palpites antes!</div>
    </div>
    """, unsafe_allow_html=True)

# ── SIDEBAR: Diagnostics ──────────────────────────────────────────────────────
with st.sidebar:
    with st.expander("🔧 Diagnostics (Debug)"):
        token_fd = st.secrets.get("FOOTBALL_DATA_TOKEN", "52974ada524e459ea4cf52a9dcc19861")
        st.write(f"**Token Football-Data:** {token_fd[:10]}...{token_fd[-5:] if len(token_fd) > 15 else ''}")
        if st.button("🔄 Limpar cache & recarregar"):
            st.cache_data.clear()
            st.rerun()
        st.write(f"**Fonte:** `{api_data.get('fonte', '?')}`")
        st.write(f"**Gols Brasil:** {api_data.get('gols_brasil', [])}")
        st.write(f"**Jogos grupos:** {len(api_data.get('jogos_reais', []))}")
        st.write(f"**Jogos mata-mata:** {len(api_data.get('jogos_mata_mata', []))}")

# ── Status fonte ──────────────────────────────────────────────────────────────
fonte_dados = api_data.get("fonte", "calendário fixo")
gols_api    = api_data.get("gols_brasil", [None] * 6)
tem_resultado_api = any(g is not None for g in gols_api)

if fonte_dados == "football-data.org" and tem_resultado_api:
    st.info(f"✅ Resultados sincronizados via **{fonte_dados}**.")
elif fonte_dados == "football-data.org":
    st.info(f"🔄 Conectado a **{fonte_dados}**, nenhum jogo finalizado ainda.")
else:
    st.info(f"📅 Usando {fonte_dados} como fonte de dados.")

# ==============================================================================
# SELEÇÃO DE USUÁRIO + AUTENTICAÇÃO PIN
# ==============================================================================
col_sel, col_pin = st.columns([2, 1])
with col_sel:
    usuario_selecionado = st.selectbox("👤 Quem é você?", AMIGOS, key="selectbox_usuario")

if "ultimo_usuario" not in st.session_state:
    st.session_state.ultimo_usuario = usuario_selecionado
if st.session_state.ultimo_usuario != usuario_selecionado:
    st.session_state.usuario_autenticado = None
    st.session_state.tentativas_pin = 0
    st.session_state.ultimo_usuario = usuario_selecionado

dados_usuario = st.session_state.banco[usuario_selecionado]
autenticado   = (st.session_state.usuario_autenticado == usuario_selecionado)
modo_view_only = not autenticado

with col_pin:
    if not autenticado:
        pin_input = st.text_input("🔑 PIN", type="password", max_chars=6,
                                  placeholder="••••", key=f"pin_{usuario_selecionado}",
                                  label_visibility="visible")
        if pin_input:
            if pin_input == PINS[usuario_selecionado]:
                banco_fresco = carregar_banco()
                st.session_state.banco = banco_fresco
                dados_usuario = st.session_state.banco[usuario_selecionado]
                st.session_state.usuario_autenticado = usuario_selecionado
                st.session_state.tentativas_pin = 0
                st.rerun()
            else:
                st.session_state.tentativas_pin += 1
                st.error(f"PIN errado ({st.session_state.tentativas_pin}x)")
    else:
        st.success(f"✅ Olá, {usuario_selecionado}!")

# ==============================================================================
# ABAS
# ==============================================================================
aba_grupos, aba_matamata, aba_calendario, aba_ranking = st.tabs(
    ["📊 Chaves & Brasil", "🌳 Mata-Mata", "📅 Calendário", "🥇 Ranking"]
)

# ──────────────────────────────────────────────────────────────────────────────
# ABA 1: CHAVES E BRASIL
# ──────────────────────────────────────────────────────────────────────────────
with aba_grupos:
    if autenticado and dados_usuario["travado"]:
        st.markdown('<div class="status-travado">🔒 Palpites travados! Boa sorte, cuzão! 🍀</div>', unsafe_allow_html=True)
    elif autenticado and not dados_usuario["travado"]:
        st.markdown('<div class="status-editando">✏️ Editando — defina a classificação de cada grupo e trave antes do 1º jogo!</div>', unsafe_allow_html=True)
    elif not autenticado and dados_usuario["travado"]:
        st.markdown('<div class="status-travado">🔒 Palpites travados — visualizando como convidado.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="view-banner">👁 Modo visualização — faça login com seu PIN para editar seus palpites</div>', unsafe_allow_html=True)

    travado_ou_view = dados_usuario["travado"] or modo_view_only
    palpites_grupos = {}

    st.markdown("## 📊 Classificação dos Grupos")

    for nome_grupo, lista_times in GRUPOS_CONFIG.items():
        st.markdown(f'<div class="group-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="group-header">{nome_grupo}</div>', unsafe_allow_html=True)

        ordem = list(dados_usuario["classificacao"].get(nome_grupo, lista_times))
        times_faltando = [t for t in lista_times if t not in ordem]
        ordem = [t for t in ordem if t in lista_times] + times_faltando

        if travado_ou_view:
            if dados_usuario["travado"]:
                st.markdown(
                    f"🥇 **{ordem[0]}** &nbsp;|&nbsp; 🥈 **{ordem[1]}** &nbsp;|&nbsp; "
                    f"🥉 {ordem[2]} &nbsp;|&nbsp; ❌ {ordem[3]}",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<span style='color:#94a3b8;font-size:13px;'>🔒 Faça login para ver e editar seus palpites</span>",
                    unsafe_allow_html=True
                )
            palpites_grupos[nome_grupo] = ordem
        else:
            col1, col2 = st.columns(2)
            t1 = col1.selectbox("🥇 1º", lista_times, index=lista_times.index(ordem[0]), key=f"t1_{nome_grupo}")
            if t1 != ordem[0]:
                idx = ordem.index(t1); ordem[idx] = ordem[0]; ordem[0] = t1
                dados_usuario["classificacao"][nome_grupo] = ordem; st.rerun()
            opcoes_2 = [t for t in lista_times if t != t1]
            t2 = col2.selectbox("🥈 2º", opcoes_2,
                                index=opcoes_2.index(ordem[1]) if ordem[1] in opcoes_2 else 0,
                                key=f"t2_{nome_grupo}")
            if t2 != ordem[1]:
                idx = ordem.index(t2); ordem[idx] = ordem[1]; ordem[1] = t2
                dados_usuario["classificacao"][nome_grupo] = ordem; st.rerun()
            opcoes_3 = [t for t in lista_times if t != t1 and t != t2]
            t3 = col1.selectbox("🥉 3º", opcoes_3,
                                index=opcoes_3.index(ordem[2]) if ordem[2] in opcoes_3 else 0,
                                key=f"t3_{nome_grupo}")
            if t3 != ordem[2]:
                idx = ordem.index(t3); ordem[idx] = ordem[2]; ordem[2] = t3
                dados_usuario["classificacao"][nome_grupo] = ordem; st.rerun()
            t4 = [t for t in lista_times if t not in [t1, t2, t3]][0]
            ordem[3] = t4
            col2.markdown(f"<p style='margin-top:28px;font-size:13px;color:#94a3b8;'>❌ 4º: {t4}</p>", unsafe_allow_html=True)
            dados_usuario["classificacao"][nome_grupo] = [t1, t2, t3, t4]
            palpites_grupos[nome_grupo] = [t1, t2, t3, t4]

        jogos_com_placar = _jogos_do_grupo(nome_grupo, apenas_com_placar=True)
        if jogos_com_placar:
            atual = api_data["classificacao_real"].get(nome_grupo, lista_times)
            ordem_atual = " &nbsp;|&nbsp; ".join(f"{p + 1}º {t}" for p, t in enumerate(atual))
            linhas_res = "".join(
                f'<div class="real-line">⚽ {_formatar_placar(j)} '
                f'<span style="color:#94a3b8;">({j.get("fonte_resultado", api_data["fonte"])})</span></div>'
                for j in jogos_com_placar
            )
            st.markdown(f'<div class="real-box"><div class="real-title">Classificação atual</div>'
                        f'<div class="real-line">{ordem_atual}</div>{linhas_res}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="real-box"><div class="real-title">Classificação atual</div>'
                        '<div class="real-line">Aguardando resultados com placar.</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Jogos do Brasil ──────────────────────────────────────────────────────
    st.markdown("## 🇧🇷 Jogos do Brasil — Grupo C")
    palpites_gols = list(dados_usuario["placar_brasil"])

    for idx, jogo_info in enumerate(JOGOS_BRASIL):
        st.markdown(f'<div class="group-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="group-header-br">🗓 {jogo_info["jogo"]} — {jogo_info["data"]} {jogo_info["hora"]}</div>', unsafe_allow_html=True)
        st.caption(f"📍 {jogo_info['loc']}")
        b = idx * 2

        gols_api_br = api_data.get("gols_brasil", [None] * 6)
        tem_res_api = gols_api_br[b] is not None and gols_api_br[b + 1] is not None
        jogo_fin_api = any(jogo_info["jogo"] in j["jogo"] and j.get("status") == "FINISHED"
                           for j in api_data.get("jogos_reais", []))
        badge_fonte = ""
        if tem_res_api and jogo_fin_api:
            badge_fonte = '<span style="color:#15803d;font-size:11px;font-weight:600;">✅ Football-Data.org</span>'
        else:
            rm = _resultados_manuais()
            if rm.get(jogo_info["jogo"], {}).get("placar_c") is not None:
                badge_fonte = '<span style="color:#ca8a04;font-size:11px;font-weight:600;">✏️ Preenchimento manual</span>'

        if travado_ou_view:
            if dados_usuario["travado"]:
                g_br_s  = int(dados_usuario["placar_brasil"][b])
                g_adv_s = int(dados_usuario["placar_brasil"][b + 1])
                st.markdown(
                    f"<div style='text-align:center;font-size:22px;font-weight:800;color:#15803d;padding:8px 0;'>"
                    f"🇧🇷 Brasil {g_br_s} × {g_adv_s} Adversário</div>", unsafe_allow_html=True)
                palpites_gols[b] = g_br_s; palpites_gols[b + 1] = g_adv_s
            else:
                st.markdown("<span style='color:#94a3b8;font-size:13px;'>🔒 Faça login para ver e editar seus palpites de placar</span>", unsafe_allow_html=True)
        else:
            c1, c2 = st.columns(2)
            g_br  = c1.number_input("Gols Brasil", min_value=0, max_value=20,
                                    value=int(dados_usuario["placar_brasil"][b]), step=1, key=f"gbr_{idx}")
            g_adv = c2.number_input("Gols Adversário", min_value=0, max_value=20,
                                    value=int(dados_usuario["placar_brasil"][b + 1]), step=1, key=f"gadv_{idx}")
            palpites_gols[b] = g_br; palpites_gols[b + 1] = g_adv

        # Resultado real
        r_br  = api_data.get("gols_brasil", [None]*6)[b]
        r_adv = api_data.get("gols_brasil", [None]*6)[b + 1]
        t_c, t_f = _partes_jogo(jogo_info["jogo"])
        adversario = t_f if t_c == "Brasil" else t_c

        if r_br is not None and r_adv is not None:
            placar_str = (f"Brasil {r_br} × {r_adv} {adversario}" if t_c == "Brasil"
                          else f"{adversario} {r_adv} × {r_br} Brasil")
            fonte_str = badge_fonte or f'<span style="color:#94a3b8;font-size:11px;">{api_data["fonte"]}</span>'
            st.markdown(f'<div class="real-box"><div class="real-title">Resultado real</div>'
                        f'<div class="real-line">⚽ {placar_str} {fonte_str}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="real-box"><div class="real-title">Resultado real</div>'
                        '<div class="real-line">Aguardando resultado.</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Botão de Trava ────────────────────────────────────────────────────────
    if autenticado and not dados_usuario["travado"]:
        st.write("---")
        chave_trava = f"disparar_trava_{usuario_selecionado}"
        if chave_trava not in st.session_state:
            st.session_state[chave_trava] = False
        if not st.session_state[chave_trava]:
            if st.button("🚨 Salvar palpites definitivos", key="btn_salvar"):
                st.session_state[chave_trava] = True; st.rerun()
        else:
            st.markdown('<div class="cuzao-box"><p class="cuzao-title">⚠️ Tem certeza, cuzão?</p>'
                        '<p class="cuzao-sub">Depois disso não dá pra editar mais nada. Juro.</p></div>', unsafe_allow_html=True)
            col_sim, col_nao = st.columns(2)
            if col_sim.button("🔥 Sim, quero travar!", key="btn_sim"):
                banco_atual = carregar_banco()
                if banco_atual[usuario_selecionado]["travado"]:
                    st.warning("Seus palpites já estavam travados.")
                else:
                    banco_atual[usuario_selecionado]["classificacao"] = {g: list(palpites_grupos.get(g, v)) for g, v in GRUPOS_CONFIG.items()}
                    banco_atual[usuario_selecionado]["placar_brasil"]  = palpites_gols
                    banco_atual[usuario_selecionado]["travado"]        = True
                    ok = salvar_banco(banco_atual)
                    if ok:
                        st.success("✅ Palpites travados! Boa sorte! 🍀")
                    else:
                        st.error("Falha ao salvar.")
                st.session_state[chave_trava] = False; st.rerun()
            if col_nao.button("❌ Não, quero revisar", key="btn_nao"):
                st.session_state[chave_trava] = False; st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# ABA 2: MATA-MATA
# ──────────────────────────────────────────────────────────────────────────────
with aba_matamata:
    st.markdown("## 🌳 Mata-Mata — Copa 2026")

    if not MATA_MATA_LIBERADO:
        st.info("🔒 Esta aba ficará disponível após o encerramento da fase de grupos.")
    else:
        # Coletores locais para o botão de salvar
        palpites_mm_venc   = dict(dados_usuario["vencedores_mata_mata"])
        palpites_mm_placar = {k: list(v) if isinstance(v, list) else [0, 0]
                              for k, v in dados_usuario["palpites_placar_mm"].items()}

        # ======================================================================
        # FUNÇÃO AUXILIAR: renderiza uma fase
        # ======================================================================
        def _render_fase_mm(nome_fase, confrontos_pares, campo_trava,
                             fase_liberada, fase_anterior_ok, prefixo):
            """
            confrontos_pares: list of (conf_def_ou_None, conf_label_dict)
            """
            st.markdown(f'<div class="mm-fase-header">🏆 {nome_fase}</div>', unsafe_allow_html=True)
            usuario_travou = dados_usuario.get(campo_trava, False)

            if not fase_liberada and not fase_anterior_ok:
                st.markdown('<div class="mm-fase-locked">🔒 Disponível após o encerramento da fase anterior</div>', unsafe_allow_html=True)
                return

            if usuario_travou:
                st.markdown('<div class="status-travado" style="margin-bottom:10px;">🔒 Palpites desta fase travados!</div>', unsafe_allow_html=True)

            cols = st.columns(2)

            for i, (conf_def, conf_label) in enumerate(confrontos_pares):
                cid = conf_label["id"]
                titulo_fase = conf_label.get("label", f"Confronto {cid}")

                # Resolve nomes reais dos times
                if conf_def is not None:
                    t1_d, t2_d = _resolver_times_oitava(conf_def, conf_label)
                else:
                    t1_d = conf_label["t1"]
                    t2_d = conf_label["t2"]

                with cols[i % 2]:
                    st.markdown(f'<div class="mm-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="mm-id">{titulo_fase} — {cid}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="mm-times">⚽ {t1_d} <span style="color:#94a3b8;">vs</span> {t2_d}</div>', unsafe_allow_html=True)

                    pode_editar = (autenticado and not usuario_travou
                                   and (fase_liberada or fase_anterior_ok))

                    venc_atual = palpites_mm_venc.get(cid, "")
                    opcoes = ["— escolher —", t1_d, t2_d]
                    # Normaliza: venc salvo pode ser nome antigo (placeholder)
                    idx_venc = 0
                    for oi, op in enumerate(opcoes):
                        if op and venc_atual and _normalizar_time(op) == _normalizar_time(venc_atual):
                            idx_venc = oi; break

                    if pode_editar:
                        novo_venc = st.radio(
                            "Quem avança?", options=opcoes, index=idx_venc,
                            key=f"{prefixo}_v_{cid}", horizontal=True, label_visibility="collapsed"
                        )
                        palpites_mm_venc[cid] = novo_venc if novo_venc != "— escolher —" else ""

                        # Palpite de placar
                        c1, c2 = st.columns(2)
                        pl = palpites_mm_placar.get(cid, [0, 0])
                        g1 = c1.number_input(f"{t1_d[:10]}", min_value=0, max_value=20,
                                             value=int(pl[0]), step=1, key=f"{prefixo}_g1_{cid}")
                        g2 = c2.number_input(f"{t2_d[:10]}", min_value=0, max_value=20,
                                             value=int(pl[1]), step=1, key=f"{prefixo}_g2_{cid}")
                        palpites_mm_placar[cid] = [g1, g2]
                    else:
                        # Exibe palpite salvo
                        if venc_atual and venc_atual != "— escolher —":
                            pl = dados_usuario["palpites_placar_mm"].get(cid, [0, 0])
                            pl_txt = (f" ({pl[0]}×{pl[1]})" if isinstance(pl, list) and len(pl) >= 2
                                      and usuario_travou else "")
                            st.markdown(f"✅ **Palpite:** {venc_atual}{pl_txt}", unsafe_allow_html=True)
                        elif not autenticado:
                            st.markdown("<span style='color:#94a3b8;font-size:12px;'>🔒 Login para palpitar</span>", unsafe_allow_html=True)
                        else:
                            st.markdown("<span style='color:#94a3b8;font-size:12px;'>Sem palpite registrado</span>", unsafe_allow_html=True)

                    # Resultado real abaixo do card
                    resultado_r = _resultado_mm(cid, t1_d, t2_d)
                    if resultado_r:
                        gc_r = resultado_r.get("placar_c")
                        gf_r = resultado_r.get("placar_f")
                        vr   = resultado_r.get("vencedor", "")
                        if gc_r is not None and gf_r is not None:
                            placar_real_str = f"{t1_d} {gc_r} × {gf_r} {t2_d}"
                            venc_badge = f" — <strong>Avança: {vr}</strong>" if vr else ""
                            st.markdown(
                                f'<div class="mm-real-result">📊 {placar_real_str}{venc_badge} '
                                f'<span style="color:#94a3b8;font-size:10px;">({resultado_r.get("fonte","")})</span></div>',
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown('<div class="mm-real-result">⏳ Aguardando resultado</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="mm-real-result">⏳ Jogo ainda não realizado</div>', unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

            # Botão de trava / rascunho desta fase
            if autenticado and not usuario_travou and (fase_liberada or fase_anterior_ok):
                st.write("")
                chave_f = f"trava_fase_{prefixo}_{usuario_selecionado}"
                if chave_f not in st.session_state:
                    st.session_state[chave_f] = False

                col_r, col_t = st.columns([1, 1])
                # Salvar rascunho
                if col_r.button(f"💾 Rascunho", key=f"rascunho_{prefixo}"):
                    banco_at = carregar_banco()
                    banco_at[usuario_selecionado]["vencedores_mata_mata"].update(palpites_mm_venc)
                    banco_at[usuario_selecionado]["palpites_placar_mm"].update(
                        {k: list(v) for k, v in palpites_mm_placar.items()})
                    if salvar_banco(banco_at):
                        st.success("💾 Rascunho salvo!")
                    else:
                        st.error("Falha ao salvar.")

                # Travar fase
                if not st.session_state[chave_f]:
                    if col_t.button(f"🔒 Travar {nome_fase}", key=f"trava_{prefixo}"):
                        st.session_state[chave_f] = True; st.rerun()
                else:
                    st.markdown('<div class="cuzao-box"><p class="cuzao-title">⚠️ Travar esta fase?</p>'
                                '<p class="cuzao-sub">Não dá pra editar depois!</p></div>', unsafe_allow_html=True)
                    cs, cn = st.columns(2)
                    if cs.button(f"🔥 Sim, travar!", key=f"sim_{prefixo}"):
                        banco_at = carregar_banco()
                        banco_at[usuario_selecionado]["vencedores_mata_mata"].update(palpites_mm_venc)
                        banco_at[usuario_selecionado]["palpites_placar_mm"].update(
                            {k: list(v) for k, v in palpites_mm_placar.items()})
                        banco_at[usuario_selecionado][campo_trava] = True
                        if salvar_banco(banco_at):
                            st.success(f"✅ {nome_fase} travado!")
                            dados_usuario[campo_trava] = True
                        else:
                            st.error("Falha ao salvar.")
                        st.session_state[chave_f] = False; st.rerun()
                    if cn.button("❌ Cancelar", key=f"nao_{prefixo}"):
                        st.session_state[chave_f] = False; st.rerun()

        # ======================================================================
        # Resolve nomes reais para oitavas e monta pares
        # ======================================================================
        oitavas_pares = list(zip(MATA_MATA_OITAVAS_DEF, MATA_MATA_OITAVAS_LABELS))
        quartas_pares = [(None, c) for c in MATA_MATA_QUARTAS]
        semis_pares   = [(None, c) for c in MATA_MATA_SEMIS]
        final_pares   = [(None, c) for c in MATA_MATA_FINAL]

        _render_fase_mm("Oitavas de Final", oitavas_pares,
                        "mm_oitavas_travadas", MATA_MATA_LIBERADO, True, "oitavas")
        _render_fase_mm("Quartas de Final", quartas_pares,
                        "mm_quartas_travadas", QUARTAS_LIBERADAS,
                        dados_usuario.get("mm_oitavas_travadas", False), "quartas")
        _render_fase_mm("Semifinais", semis_pares,
                        "mm_semis_travadas", SEMIS_LIBERADAS,
                        dados_usuario.get("mm_quartas_travadas", False), "semis")
        _render_fase_mm("Final e 3º Lugar", final_pares,
                        "mm_final_travada", FINAL_LIBERADA,
                        dados_usuario.get("mm_semis_travadas", False), "final")

        # ======================================================================
        # ÁRVORE VISUAL
        # ======================================================================
        st.markdown("---")
        st.markdown("## 🌳 Árvore do Chaveamento")
        st.caption("Mostra os confrontos e o progresso. 🟢 = resultado real · 🔵 = seu palpite de vencedor")

        pv = dados_usuario["vencedores_mata_mata"]
        res_mm_cache = {}
        def _get_res(cid, t1, t2):
            if cid not in res_mm_cache:
                res_mm_cache[cid] = _resultado_mm(cid, t1, t2)
            return res_mm_cache[cid]

        def _card_arvore(cid, t1, t2, label=""):
            res = _get_res(cid, t1, t2)
            vp  = pv.get(cid, "")
            rv  = res.get("vencedor", "") if res else ""
            gc  = res.get("placar_c", "") if res else ""
            gf  = res.get("placar_f", "") if res else ""
            t1s = (t1 or "?")[:14]
            t2s = (t2 or "?")[:14]
            cor1 = ("#15803d" if rv and _normalizar_time(rv) == _normalizar_time(t1)
                    else ("#1d4ed8" if vp and _normalizar_time(vp) == _normalizar_time(t1)
                    else "#334155"))
            cor2 = ("#15803d" if rv and _normalizar_time(rv) == _normalizar_time(t2)
                    else ("#1d4ed8" if vp and _normalizar_time(vp) == _normalizar_time(t2)
                    else "#334155"))
            placar_html = (f'<div style="font-size:11px;font-weight:800;color:#1d4ed8;text-align:center;">'
                           f'{gc}×{gf}</div>' if gc != "" and gf != "" else "")
            return (f'<div style="background:#fff;border:1.5px solid #e2e8f0;border-radius:8px;'
                    f'padding:5px 8px;margin:2px 0;min-width:120px;">'
                    f'<div style="font-size:9px;color:#94a3b8;font-weight:700;text-align:center;'
                    f'margin-bottom:1px;">{label or cid}</div>'
                    f'<div style="font-size:10px;font-weight:700;color:{cor1};text-align:center;">{t1s}</div>'
                    f'<div style="font-size:9px;color:#94a3b8;text-align:center;">vs</div>'
                    f'<div style="font-size:10px;font-weight:700;color:{cor2};text-align:center;">{t2s}</div>'
                    f'{placar_html}</div>')

        # Resolve nomes reais de oitavas para a árvore
        def _t(conf_def, lbl):
            if conf_def:
                return _resolver_times_oitava(conf_def, lbl)
            return lbl["t1"], lbl["t2"]

        col_o1, col_o2, col_q, col_s, col_f = st.columns([2, 2, 2, 2, 2])

        oitavas_esq = list(zip(MATA_MATA_OITAVAS_DEF[:8], MATA_MATA_OITAVAS_LABELS[:8]))
        oitavas_dir = list(zip(MATA_MATA_OITAVAS_DEF[8:], MATA_MATA_OITAVAS_LABELS[8:]))

        with col_o1:
            st.markdown("**Oitavas ①**")
            for cd, cl in oitavas_esq:
                t1, t2 = _t(cd, cl)
                st.markdown(_card_arvore(cl["id"], t1, t2), unsafe_allow_html=True)

        with col_o2:
            st.markdown("**Oitavas ②**")
            for cd, cl in oitavas_dir:
                t1, t2 = _t(cd, cl)
                st.markdown(_card_arvore(cl["id"], t1, t2), unsafe_allow_html=True)

        with col_q:
            st.markdown("**Quartas**")
            for c in MATA_MATA_QUARTAS:
                st.markdown(_card_arvore(c["id"], c["t1"], c["t2"]), unsafe_allow_html=True)

        with col_s:
            st.markdown("**Semis**")
            for c in MATA_MATA_SEMIS:
                st.markdown(_card_arvore(c["id"], c["t1"], c["t2"]), unsafe_allow_html=True)

        with col_f:
            st.markdown("**Final**")
            for c in MATA_MATA_FINAL:
                st.markdown(_card_arvore(c["id"], c["t1"], c["t2"], c.get("label", c["id"])),
                            unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# ABA 3: CALENDÁRIO
# ──────────────────────────────────────────────────────────────────────────────
with aba_calendario:
    st.markdown("## 📅 Calendário da Copa 2026")
    st.markdown(f'<div class="fonte-dados">Fonte: {api_data["fonte"]}</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        filtro_brasil = st.toggle("🇧🇷 Só jogos do Brasil", value=False, key="filtro_br")
    with col_f2:
        filtro_sel = st.selectbox("Filtrar por seleção:", ["Todas"] + sorted({
            t for j in CALENDARIO_FIXO for t in j["jogo"].replace(" x ", "|").split("|")
        }), key="filtro_sel")

    jogos_exibir = CALENDARIO_FIXO
    if filtro_brasil:
        jogos_exibir = [j for j in jogos_exibir if j["brasil"]]
    if filtro_sel != "Todas":
        jogos_exibir = [j for j in jogos_exibir if filtro_sel in j["jogo"]]

    datas = list(dict.fromkeys(j["data"] for j in jogos_exibir))
    for data in datas:
        st.markdown(f'<div class="data-header">📆 {data}</div>', unsafe_allow_html=True)
        for j in [x for x in jogos_exibir if x["data"] == data]:
            jogo_real = _buscar_jogo_real(j["jogo"])
            status = _status_jogo(j["data"], j["hora"])
            if jogo_real:
                if jogo_real.get("status") == "FINISHED":   status = "finalizado"
                elif jogo_real.get("status") == "IN_PLAY":  status = "aovivo"
            nome_jogo = _formatar_placar(jogo_real) if jogo_real and _tem_placar(jogo_real) else j["jogo"]
            fonte_resultado = (f' · {jogo_real.get("fonte_resultado", api_data["fonte"])}'
                               if jogo_real and _tem_placar(jogo_real) else "")
            brasil_class = "jogo-brasil" if j["brasil"] else ""
            badge = ('<span class="badge-finalizado">✓ Finalizado</span>' if status == "finalizado"
                     else '<span class="badge-aovivo">🔴 Ao vivo</span>' if status == "aovivo"
                     else '<span class="badge-previsto">Previsto</span>')
            st.markdown(f"""
            <div class="jogo-card {brasil_class}">
                <div class="jogo-data">{j["data"]}</div>
                <div class="jogo-hora">{j["hora"]}</div>
                <div>
                    <div class="jogo-nome">{nome_jogo}</div>
                    <div class="jogo-local">📍 {j["local"]}{fonte_resultado}</div>
                </div>
                {badge}
            </div>
            """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# ABA 4: RANKING
# ──────────────────────────────────────────────────────────────────────────────
with aba_ranking:
    st.markdown("## 🥇 Ranking Geral")

    with st.expander("📋 Regras de pontuação"):
        st.markdown("""
        <div class="regra-box">
            <div class="regra-item"><strong>Fase de Grupos</strong></div>
            <div class="regra-item">🥇 1º colocado correto no grupo: <strong>+2 pts</strong></div>
            <div class="regra-item">🥈 2º colocado correto no grupo: <strong>+2 pts</strong></div>
            <div class="regra-item">⚽ Placar exato do Brasil (fase grupos): <strong>+5 pts</strong></div>
            <div class="regra-item">✅ Resultado correto (Brasil, fase grupos): <strong>+3 pts</strong></div>
            <div class="regra-item" style="margin-top:8px;"><strong>Mata-Mata (todas as fases)</strong></div>
            <div class="regra-item">⚽ Placar exato: <strong>+5 pts</strong></div>
            <div class="regra-item">✅ Acertar quem avança: <strong>+3 pts</strong></div>
            <div class="regra-item">❌ Errar: <strong>0 pts</strong></div>
            <div class="regra-item" style="margin-top:8px;">🔒 Palpite não travado: <strong>0 pts</strong></div>
        </div>
        """, unsafe_allow_html=True)

    linhas = []
    qualquer_jogo_realizado = any(j.get("status") == "FINISHED" for j in api_data.get("jogos_reais", []))

    for amigo in AMIGOS:
        user  = st.session_state.banco[amigo]
        total, detalhes = _calcular_pontuacao(amigo)
        travado = user["travado"]
        badges = []
        if travado:
            acertou_placar = any(
                user["placar_brasil"][i*2] == api_data["gols_brasil"][i*2] and
                user["placar_brasil"][i*2+1] == api_data["gols_brasil"][i*2+1] and
                api_data["gols_brasil"][i*2] is not None
                for i in range(3)
            )
            if acertou_placar: badges.append("🔮 Profeta")
            if qualquer_jogo_realizado and total == 0: badges.append("🤡 Zica")
        linhas.append({"amigo": amigo, "total": total, "travado": travado,
                        "badges": badges, "detalhes": detalhes})

    linhas.sort(key=lambda x: (-int(x["travado"]), -x["total"]))
    travados_com_pts = [l for l in linhas if l["travado"] and l["total"] > 0]
    if travados_com_pts:
        linhas[0]["badges"].insert(0, "👑 Líder")
        if len(travados_com_pts) > 1:
            linhas[-1]["badges"].append("🔦 Lanterna")

    pos_icons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣"]
    for i, linha in enumerate(linhas):
        cor_borda = "border: 2px solid #1d4ed8;" if i == 0 and linha["total"] > 0 else ""
        badge_str = " | ".join(linha["badges"]) if linha["badges"] else (
            "⏳ Aguardando início" if not qualquer_jogo_realizado else "🏃 Em jogo")
        status_str = "🔒 Travado" if linha["travado"] else "🔓 Editando"
        pts_color  = "#1e3a5f" if linha["total"] > 0 else "#94a3b8"
        st.markdown(f"""
        <div class="rank-row" style="{cor_borda}">
            <div class="rank-pos">{pos_icons[i]}</div>
            <div style="flex:1">
                <div class="rank-nome">{linha["amigo"]}</div>
                <div class="rank-badges">{badge_str}</div>
                <div class="{'rank-status-lock' if linha['travado'] else 'rank-status-open'}">{status_str}</div>
            </div>
            <div>
                <div class="rank-pts" style="color:{pts_color}">{linha["total"]}</div>
                <div class="rank-pts-label">pts</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if not qualquer_jogo_realizado:
        st.info("⏳ A pontuação começa após o primeiro jogo da Copa.")

    st.markdown("---")
    st.markdown("### Detalhamento por amigo")
    for linha in linhas:
        if linha["travado"] and linha["detalhes"]:
            with st.expander(f"{linha['amigo']} — {linha['total']} pts"):
                for det in linha["detalhes"]:
                    st_ = det.get("status", "wait")
                    icon = "✅" if st_ == "ok" else ("❌" if st_ == "err" else "⏳")
                    cls  = "detail-ok" if st_ == "ok" else ("detail-err" if st_ == "err" else "detail-wait")
                    st.markdown(
                        f'{icon} <strong>{det["cat"]}</strong> — {det["texto"]} '
                        f'<span class="{cls}">+{det["pts"]} pts</span>',
                        unsafe_allow_html=True
                    )
        elif not linha["travado"]:
            with st.expander(f"{linha['amigo']} — palpite em aberto"):
                st.caption("Ainda não travou os palpites.")
