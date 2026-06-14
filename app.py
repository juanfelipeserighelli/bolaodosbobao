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

/* ── Mata-mata ── */
.mm-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 11px 14px; margin-bottom: 8px;
}
.mm-id { font-size: 10px; color: #94a3b8; font-weight: 600;
    text-transform: uppercase; margin-bottom: 4px; }
.mm-times { font-size: 13px; font-weight: 600; color: #334155; }

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

MATA_MATA_CONFRONTOS = [
    {"id": "M1",  "t1": "1º E", "t2": "3º colocado"},
    {"id": "M2",  "t1": "1º I", "t2": "3º colocado"},
    {"id": "M3",  "t1": "2º A", "t2": "2º B"},
    {"id": "M4",  "t1": "1º F", "t2": "2º C"},
    {"id": "M5",  "t1": "2º K", "t2": "2º L"},
    {"id": "M6",  "t1": "1º H", "t2": "2º J"},
    {"id": "M7",  "t1": "1º D", "t2": "3º colocado"},
    {"id": "M8",  "t1": "1º G", "t2": "3º colocado"},
    {"id": "M9",  "t1": "1º C", "t2": "2º F"},
    {"id": "M10", "t1": "2º E", "t2": "2º I"},
    {"id": "M11", "t1": "1º A", "t2": "3º colocado"},
    {"id": "M12", "t1": "1º L", "t2": "3º colocado"},
    {"id": "M13", "t1": "1º J", "t2": "2º H"},
    {"id": "M14", "t1": "2º D", "t2": "2º G"},
    {"id": "M15", "t1": "1º B", "t2": "3º colocado"},
    {"id": "M16", "t1": "1º K", "t2": "3º colocado"},
]

# Libera aba do mata-mata para edição quando os confrontos reais forem definidos
MATA_MATA_LIBERADO = False

BRT = timezone(timedelta(hours=-3))
DURACAO_JOGO_MIN = 110

# Próximo jogo do Brasil para o countdown
PROXIMO_JOGO_BRASIL = {
    "nome":  "Brasil x Marrocos",
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
# BANCO DE DADOS — JSONBin.io  (única fonte da verdade)
# ==============================================================================
def _jsonbin_headers():
    key = st.secrets.get("JSONBIN_KEY", "")
    return {"Content-Type": "application/json", "X-Master-Key": key}

def _jsonbin_url():
    bin_id = st.secrets.get("JSONBIN_ID", "")
    return f"https://api.jsonbin.io/v3/b/{bin_id}"

def _banco_padrao():
    banco = {}
    for amigo in AMIGOS:
        banco[amigo] = {
            "travado": False,
            "classificacao": {g: list(t) for g, t in GRUPOS_CONFIG.items()},
            "placar_brasil": [0, 0, 0, 0, 0, 0],
            "vencedores_mata_mata": {c["id"]: "" for c in MATA_MATA_CONFRONTOS},
        }
    return banco

def carregar_banco():
    """
    Busca o banco do JSONBin.
    - Se o bin estiver vazio ou com estrutura antiga, inicializa/completa com padrão.
    - Retorna banco completo ou padrão em caso de falha de conexão.
    """
    banco_seguro = _banco_padrao()
    try:
        bin_id  = st.secrets.get("JSONBIN_ID", "")
        api_key = st.secrets.get("JSONBIN_KEY", "")
        if not bin_id or not api_key:
            return banco_seguro

        resp = requests.get(_jsonbin_url(), headers=_jsonbin_headers(), timeout=6)

        if resp.status_code == 200:
            dados = resp.json().get("record", {})

            # Bin vazio ou inicializado com estrutura errada → grava o padrão
            if not dados or not isinstance(dados, dict) or not any(a in dados for a in AMIGOS):
                requests.put(_jsonbin_url(), json=banco_seguro, headers=_jsonbin_headers(), timeout=8)
                return banco_seguro

            for amigo in AMIGOS:
                if amigo in dados:
                    d = dados[amigo]
                    banco_seguro[amigo]["travado"]              = bool(d.get("travado", False))
                    banco_seguro[amigo]["classificacao"]        = d.get("classificacao",        banco_seguro[amigo]["classificacao"])
                    banco_seguro[amigo]["placar_brasil"]        = d.get("placar_brasil",        banco_seguro[amigo]["placar_brasil"])
                    banco_seguro[amigo]["vencedores_mata_mata"] = d.get("vencedores_mata_mata", banco_seguro[amigo]["vencedores_mata_mata"])

            return banco_seguro

        if resp.status_code in (401, 403):
            st.warning("⚠️ JSONBin: chave de API inválida. Rodando em modo local (palpites não salvos na nuvem).")
        elif resp.status_code == 404:
            st.warning("⚠️ JSONBin: bin não encontrado. Verifique o JSONBIN_ID nos secrets.")

    except requests.exceptions.Timeout:
        st.warning("⚠️ JSONBin sem resposta (timeout). Rodando com dados locais.")
    except Exception:
        pass

    return banco_seguro

def salvar_banco(banco_completo):
    """
    Grava o banco completo no JSONBin via PUT.
    PROTEÇÃO: antes de salvar, compara com o banco remoto e nunca
    sobrescreve palpites de usuários travados com dados da API.
    """
    try:
        bin_id  = st.secrets.get("JSONBIN_ID", "")
        api_key = st.secrets.get("JSONBIN_KEY", "")
        if not bin_id or not api_key:
            st.session_state.banco = banco_completo
            return True

        # ── Busca o banco remoto atual para proteção ──────────────────────
        resp_atual = requests.get(_jsonbin_url(), headers=_jsonbin_headers(), timeout=6)
        if resp_atual.status_code == 200:
            banco_remoto = resp_atual.json().get("record", {})
            for amigo in AMIGOS:
                if banco_remoto.get(amigo, {}).get("travado"):
                    # Usuário travado: preserva classificacao e placar_brasil remotos
                    banco_completo[amigo]["classificacao"]  = banco_remoto[amigo]["classificacao"]
                    banco_completo[amigo]["placar_brasil"]  = banco_remoto[amigo]["placar_brasil"]
                    banco_completo[amigo]["travado"]        = True

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
# INICIALIZAÇÃO DO SESSION_STATE — carrega do JSONBin UMA vez por sessão
# ==============================================================================
if "banco" not in st.session_state:
    st.session_state.banco = carregar_banco()

# Garante que nenhum amigo fique de fora (segurança contra banco antigo)
padrao = _banco_padrao()
for amigo in AMIGOS:
    if amigo not in st.session_state.banco:
        st.session_state.banco[amigo] = padrao[amigo]

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
    "Bosnia and Herzegovina": "Bósnia", "Canada": "Canadá", "Qatar": "Catar", "Switzerland": "Suíça",
    "Australia": "Austrália", "Paraguay": "Paraguai", "Turkey": "Turquia",
    "USA": "Estados Unidos", "United States": "Estados Unidos",
    "Curaçao": "Curaçao", "Ecuador": "Equador", "Germany": "Alemanha",
    "Ivory Coast": "Costa do Marfim", "Cote d'Ivoire": "Costa do Marfim",
    "Japan": "Japão", "Netherlands": "Países Baixos", "Sweden": "Suécia", "Tunisia": "Tunísia",
    "Belgium": "Bélgica", "Egypt": "Egito", "Iran": "Irã", "New Zealand": "Nova Zelândia",
    "Cape Verde": "Cabo Verde", "Cape Verde Islands": "Cabo Verde", "Saudi Arabia": "Arábia Saudita", "Spain": "Espanha", "Uruguay": "Uruguai",
    "South Korea": "Coreia do Sul", "France": "França", "Iraq": "Iraque", "Norway": "Noruega", "Senegal": "Senegal",
    "Algeria": "Argélia", "Argentina": "Argentina", "Austria": "Áustria", "Jordan": "Jordânia",
    "Colombia": "Colômbia", "DR Congo": "RD Congo", "Congo DR": "RD Congo", "Portugal": "Portugal", "Uzbekistan": "Uzbequistão",
    "Croatia": "Croácia", "England": "Inglaterra", "Ghana": "Gana", "Panama": "Panamá",
    "Bosnia-Herzegovina": "Bósnia e Herzegovina", "Curaçao": "Curaçao", "Curaþao": "Curaçao",
}

ALIASES_TIMES = {
    "Coreia": "República da Coreia",
    "Coreia do Sul": "República da Coreia",
    "República da Coreia": "República da Coreia",
    "Bósnia": "Bósnia e Herzegovina",
    "Bósnia e Herzegovina": "Bósnia e Herzegovina",
    "Bosnia": "Bósnia e Herzegovina",
    "Bosnia and Herzegovina": "Bósnia e Herzegovina",
    "USA": "Estados Unidos",
    "United States": "Estados Unidos",
    "United States of America": "Estados Unidos",
    "Czech Republic": "Tchéquia",
    "Czechia": "Tchéquia",
}

RESULTADOS_MANUAIS = {
    # Use quando alguma API demorar a publicar um resultado:
    "México x África do Sul": {"placar_c": 2, "placar_f": 0},
    "Tchéquia x Coreia do Sul": {"placar_c": 1, "placar_f": 2},
    "Canadá x Bósnia": {"placar_c": 1, "placar_f": 1},
    "Estados Unidos x Paraguai": {"placar_c": 4, "placar_f": 1},
    "Catar x Suíça": {"placar_c": 1, "placar_f": 1},
    "Brasil x Marrocos": {"placar_c": 1, "placar_f": 1}
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
            "jogo": jogo["jogo"],
            "placar_c": placar_manual.get("placar_c"),
            "placar_f": placar_manual.get("placar_f"),
            "status": "FINISHED" if status_cal == "finalizado" else ("IN_PLAY" if status_cal == "aovivo" else "SCHEDULED"),
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

def _grupo_tem_placar_real(nome_grupo):
    return bool(_jogos_do_grupo(nome_grupo, apenas_com_placar=True))

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
            key=lambda t: (-times[t]["pts"], -times[t]["sg"], -times[t]["gp"], times[t]["idx"])
        )
    return classificacao

def _montar_resultado(jogos_reais, fonte, classificacao_real=None):
    for jogo in jogos_reais:
        jogo.setdefault("fonte_resultado", fonte)
    jogos_reais = _aplicar_overrides_calendario(jogos_reais)

    # Gols do Brasil
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

    # Classificação final:
    # Prioridade 1 → classificacao_real da API (ordem oficial FIFA)
    # Prioridade 2 → recalculada localmente pelos gols (fallback)
    # Prioridade 3 → ordem padrão (nenhum jogo ainda)
    classificacao_calculada = _classificacao_por_jogos(jogos_reais)
    classificacao_final = {}

    for grupo in GRUPOS_CONFIG:
        if classificacao_real and grupo in classificacao_real and len(classificacao_real[grupo]) == 4:
            # API retornou ordem oficial — usa direto, sem recalcular
            classificacao_final[grupo] = classificacao_real[grupo]
        elif grupo in classificacao_calculada:
            # Fallback: recalcula pelos gols (sem desempate avançado)
            classificacao_final[grupo] = classificacao_calculada[grupo]
        else:
            classificacao_final[grupo] = list(GRUPOS_CONFIG[grupo])

    return {
        "fonte":              fonte,
        "classificacao_real": classificacao_final,
        "jogos_reais":        jogos_reais,
        "gols_brasil":        gols_brasil,
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
                # Tenta encontrar o time local pelo nome normalizado
                time_local = next(
                    (t for t in GRUPOS_CONFIG[nome_grupo] if _normalizar_time(t) == nome_norm),
                    None
                )
                if time_local:
                    ordem.append(time_local)

            if ordem:
                # Adiciona times que a API não retornou (ainda sem jogos) no final
                faltando = [t for t in GRUPOS_CONFIG[nome_grupo] if t not in ordem]
                retorno[nome_grupo] = ordem + faltando

        return retorno
    except Exception as e:
        st.warning(f"⚠️ Erro ao buscar classificação da API: {e}")
        return {}

@st.cache_data(ttl=120)
def obter_resultados():
    """
    Tenta as 3 APIs em sequência. Se todas falharem, usa calendário fixo.
    """
    padrao = {
        "fonte":              "calendário fixo",
        "classificacao_real": {g: list(t) for g, t in GRUPOS_CONFIG.items()},
        "jogos_reais":        [],
        "gols_brasil":        [None, None, None, None, None, None],
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
                    st.warning("⚠️ Football-Data retornou sem jogos. Usando dados manuais.")
                else:
                    jogos = []
                    for m in matches:
                        t_c = _normalizar_time(m["homeTeam"]["name"])
                        t_f = _normalizar_time(m["awayTeam"]["name"])
                        score = m.get("score") or {}
                        full_time = score.get("fullTime") or {}
                        placar_c = full_time.get("home", full_time.get("homeTeam"))
                        placar_f = full_time.get("away", full_time.get("awayTeam"))
                        status = m.get("status", "SCHEDULED")
                        jogos.append({
                            "jogo":     f"{t_c} x {t_f}",
                            "placar_c": placar_c,
                            "placar_f": placar_f,
                            "status":   _status_api_para_padrao(status),
                        })
                    st.success(f"✅ Football-Data: {len(jogos)} jogos processados")
                    classificacao_api = _classificacao_football_data(token)
                    return _montar_resultado(jogos, "football-data.org", classificacao_api)
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
                jogos = []
                for m in fixtures:
                    t_c = _normalizar_time(m.get("home_team", ""))
                    t_f = _normalizar_time(m.get("away_team", ""))
                    gc  = m.get("home_score")
                    gf  = m.get("away_score")
                    st_ = m.get("status", "SCHEDULED")
                    jogos.append({
                        "jogo":     f"{t_c} x {t_f}",
                        "placar_c": gc,
                        "placar_f": gf,
                        "status":   _status_api_para_padrao(st_),
                    })
                return _montar_resultado(jogos, "Zafronix Sports API")
    except Exception:
        pass

    # ── API 3: Sportmonks Football API ────────────────────────────────────────
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
                        return _montar_resultado(jogos, "Sportmonks")
    except Exception:
        pass

    jogos_fallback = _jogos_do_calendario_fixo()
    return _montar_resultado(jogos_fallback, "calendário fixo")

api_data = obter_resultados()

# ==============================================================================
# SINCRONIZAÇÃO AUTOMÁTICA — Atualiza placares do Brasil pela API
# ==============================================================================

# ==============================================================================
# HELPERS
# ==============================================================================
def _status_jogo(data_str: str, hora_str: str):
    """Retorna 'finalizado', 'aovivo' ou 'previsto' baseado na data/hora atual."""
    return _status_por_data_hora(data_str, hora_str)

def _countdown_brasil():
    """Retorna string do countdown para o próximo jogo do Brasil."""
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
    """
    Retorna um set com os nomes dos grupos que já têm ao menos
    um jogo finalizado segundo os dados da API.
    """
    finalizados = set()
    jogos_reais = api_data.get("jogos_reais", [])

    for nome_grupo, times in GRUPOS_CONFIG.items():
        for jogo in jogos_reais:
            if jogo.get("status") != "FINISHED":
                continue
            if not _tem_placar(jogo):
                continue
            t_c, t_f = _partes_jogo(jogo["jogo"])
            times_norm = {_normalizar_time(t) for t in times}
            if t_c in times_norm or t_f in times_norm:
                finalizados.add(nome_grupo)
                break

    return finalizados

def _calcular_pontuacao(amigo):
    """Calcula pontuação de um amigo. Retorna (total, detalhes)."""
    user     = st.session_state.banco[amigo]
    real     = api_data
    total    = 0
    detalhes = []

    if not user["travado"]:
        return 0, []

    grupos_ativos = _grupos_com_resultado()

    pts_grupos = 0
    for g in GRUPOS_CONFIG:
        if g not in grupos_ativos:
            continue
        palpite_1 = user["classificacao"][g][0]
        palpite_2 = user["classificacao"][g][1]
        real_1 = real["classificacao_real"][g][0]
        real_2 = real["classificacao_real"][g][1]

        acertou_1 = _normalizar_time(palpite_1) == _normalizar_time(real_1)
        pts_1 = 2 if acertou_1 else 0
        pts_grupos += pts_1
        detalhes.append({
            "cat": g,
            "texto": f"1º colocado: palpite {palpite_1}; atual {real_1}",
            "pts": pts_1,
            "status": "ok" if acertou_1 else "err",
        })

        acertou_2 = _normalizar_time(palpite_2) == _normalizar_time(real_2)
        pts_2 = 2 if acertou_2 else 0
        pts_grupos += pts_2
        detalhes.append({
            "cat": g,
            "texto": f"2º colocado: palpite {palpite_2}; atual {real_2}",
            "pts": pts_2,
            "status": "ok" if acertou_2 else "err",
        })
    total += pts_grupos

    pts_brasil = 0
    for i in range(3):
        b     = i * 2
        p_br  = user["placar_brasil"][b]
        p_adv = user["placar_brasil"][b + 1]
        r_br  = real["gols_brasil"][b]
        r_adv = real["gols_brasil"][b + 1]
        nome_jogo = JOGOS_BRASIL[i]["jogo"]
        if r_br is None or r_adv is None:
            detalhes.append({
                "cat": "Jogos do Brasil",
                "texto": f"{nome_jogo}: palpite {p_br}x{p_adv}; aguardando resultado",
                "pts": 0,
                "status": "wait",
            })
            continue
        if p_br == r_br and p_adv == r_adv:
            pts_jogo = 5
            status = "ok"
            texto = f"{nome_jogo}: placar exato, palpite {p_br}x{p_adv}; real {r_br}x{r_adv}"
        elif (
            (p_br > p_adv and r_br > r_adv) or
            (p_br < p_adv and r_br < r_adv) or
            (p_br == p_adv and r_br == r_adv)
        ):
            pts_jogo = 3
            status = "ok"
            texto = f"{nome_jogo}: vencedor/empate correto, palpite {p_br}x{p_adv}; real {r_br}x{r_adv}"
        else:
            pts_jogo = 0
            status = "err"
            texto = f"{nome_jogo}: palpite {p_br}x{p_adv}; real {r_br}x{r_adv}"
        pts_brasil += pts_jogo
        detalhes.append({
            "cat": "Jogos do Brasil",
            "texto": texto,
            "pts": pts_jogo,
            "status": status,
        })
    total += pts_brasil
    return total, detalhes

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

# ── SIDEBAR: Diagnostics ──────────────────────────────────────────────────
with st.sidebar:
    with st.expander("🔧 Diagnostics (Debug)"):
        token_fd = st.secrets.get("FOOTBALL_DATA_TOKEN", "52974ada524e459ea4cf52a9dcc19861")
        st.write(f"**Token Football-Data:** {token_fd[:10]}...{token_fd[-5:] if len(token_fd) > 15 else ''}")
        
        if st.button("🔄 Limpar cache & recarregar"):
            st.cache_data.clear()
            st.rerun()
        
        st.write(f"**Fonte de dados detectada:** `{api_data.get('fonte', '?')}`")
        st.write(f"**Gols Brasil da API:** {api_data.get('gols_brasil', [])}")
        st.write(f"**Jogos processados:** {len(api_data.get('jogos_reais', []))}")

# ── Status da sincronização automática ──────────────────────────────────────
fonte_dados = api_data.get("fonte", "calendário fixo")
gols_api = api_data.get("gols_brasil", [None] * 6)
tem_resultado_api = any(g is not None for g in gols_api)

if fonte_dados == "football-data.org" and tem_resultado_api:
    st.info(f"✅ Resultados sincronizados automaticamente via **{fonte_dados}**. Os placares dos jogos do Brasil foram atualizados.")
elif fonte_dados == "football-data.org":
    st.info(f"🔄 Conectado a **{fonte_dados}**, mas nenhum jogo finalizado ainda.")
else:
    st.info(f"📅 Usando {fonte_dados} como fonte de dados.")

# ==============================================================================
# SELEÇÃO DE USUÁRIO + AUTENTICAÇÃO PIN
# ==============================================================================
col_sel, col_pin = st.columns([2, 1])
with col_sel:
    usuario_selecionado = st.selectbox(
        "👤 Quem é você?",
        AMIGOS,
        key="selectbox_usuario"
    )

# Detecta troca de usuário: limpa autenticação anterior
if "ultimo_usuario" not in st.session_state:
    st.session_state.ultimo_usuario = usuario_selecionado
if st.session_state.ultimo_usuario != usuario_selecionado:
    st.session_state.usuario_autenticado = None
    st.session_state.tentativas_pin = 0
    st.session_state.ultimo_usuario = usuario_selecionado

# Sempre lê o estado do usuário do banco em memória
dados_usuario = st.session_state.banco[usuario_selecionado]

# Verifica autenticação
autenticado = (st.session_state.usuario_autenticado == usuario_selecionado)

# ── LÓGICA DE MODO ──────────────────────────────────────────────────────────
# modo_view_only   = True  → usuário NÃO autenticado (não pode editar nem ver PIN)
# palpite travado  = True  → mesmo autenticado, não pode editar
# A combinação (view_only=True + travado=True) deve mostrar os palpites normalmente,
# pois eles são públicos após travados. Só bloqueia a edição.
modo_view_only = not autenticado

with col_pin:
    if not autenticado:
        pin_input = st.text_input(
            "🔑 PIN",
            type="password",
            max_chars=6,
            placeholder="••••",
            key=f"pin_{usuario_selecionado}",
            label_visibility="visible"
        )
        if pin_input:
            if pin_input == PINS[usuario_selecionado]:
                # PIN correto — sincroniza com o banco remoto antes de autenticar
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

    # ── Banner de status — 4 casos possíveis ──────────────────────────────────
    if autenticado and dados_usuario["travado"]:
        # Autenticado + travado → mostra confirmação de travamento
        st.markdown(
            '<div class="status-travado">🔒 Palpites travados! Boa sorte, cuzão! 🍀</div>',
            unsafe_allow_html=True
        )
    elif autenticado and not dados_usuario["travado"]:
        # Autenticado + ainda editando
        st.markdown(
            '<div class="status-editando">✏️ Editando — defina a classificação de cada grupo e trave antes do 1º jogo!</div>',
            unsafe_allow_html=True
        )
    elif not autenticado and dados_usuario["travado"]:
        # Não autenticado, mas palpite já travado → palpites são visíveis (públicos)
        st.markdown(
            '<div class="status-travado">🔒 Palpites travados — visualizando como convidado.</div>',
            unsafe_allow_html=True
        )
    else:
        # Não autenticado + palpite ainda aberto → só mostra aviso de login
        st.markdown(
            '<div class="view-banner">👁 Modo visualização — faça login com seu PIN para editar seus palpites</div>',
            unsafe_allow_html=True
        )

    # travado_ou_view controla se os widgets ficam disabled / em modo read-only
    # IMPORTANTE: mesmo sem autenticação, se o palpite está travado os dados
    # devem ser EXIBIDOS (não escondidos). O flag só bloqueia a edição.
    travado_ou_view = dados_usuario["travado"] or modo_view_only

    palpites_grupos = {}

    st.markdown("## 📊 Classificação dos Grupos")

    for nome_grupo, lista_times in GRUPOS_CONFIG.items():
        st.markdown(f'<div class="group-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="group-header">{nome_grupo}</div>', unsafe_allow_html=True)

        ordem = list(dados_usuario["classificacao"].get(nome_grupo, lista_times))
        # Preserva a ordem salva; acrescenta times faltantes no final (migração)
        times_faltando = [t for t in lista_times if t not in ordem]
        ordem = [t for t in ordem if t in lista_times] + times_faltando

        if travado_ou_view:
            # ── Modo leitura: exibe a ordem salva ──────────────────────────
            # Distingue visualmente se o palpite foi travado ou se é padrão
            if dados_usuario["travado"]:
                st.markdown(
                    f"🥇 **{ordem[0]}** &nbsp;|&nbsp; 🥈 **{ordem[1]}** &nbsp;|&nbsp; "
                    f"🥉 {ordem[2]} &nbsp;|&nbsp; ❌ {ordem[3]}",
                    unsafe_allow_html=True
                )
            else:
                # Não autenticado e não travado: mostra ordem padrão com aviso
                st.markdown(
                    f"<span style='color:#94a3b8;font-size:13px;'>"
                    f"🔒 Faça login para ver e editar seus palpites</span>",
                    unsafe_allow_html=True
                )
            palpites_grupos[nome_grupo] = ordem
        else:
            # ── Modo edição ────────────────────────────────────────────────
            col1, col2 = st.columns(2)

            t1 = col1.selectbox("🥇 1º", lista_times,
                                index=lista_times.index(ordem[0]),
                                key=f"t1_{nome_grupo}")
            if t1 != ordem[0]:
                idx = ordem.index(t1)
                ordem[idx] = ordem[0]
                ordem[0] = t1
                dados_usuario["classificacao"][nome_grupo] = ordem
                st.rerun()

            opcoes_2 = [t for t in lista_times if t != t1]
            t2 = col2.selectbox("🥈 2º", opcoes_2,
                                index=opcoes_2.index(ordem[1]) if ordem[1] in opcoes_2 else 0,
                                key=f"t2_{nome_grupo}")
            if t2 != ordem[1]:
                idx = ordem.index(t2)
                ordem[idx] = ordem[1]
                ordem[1] = t2
                dados_usuario["classificacao"][nome_grupo] = ordem
                st.rerun()

            opcoes_3 = [t for t in lista_times if t != t1 and t != t2]
            t3 = col1.selectbox("🥉 3º", opcoes_3,
                                index=opcoes_3.index(ordem[2]) if ordem[2] in opcoes_3 else 0,
                                key=f"t3_{nome_grupo}")
            if t3 != ordem[2]:
                idx = ordem.index(t3)
                ordem[idx] = ordem[2]
                ordem[2] = t3
                dados_usuario["classificacao"][nome_grupo] = ordem
                st.rerun()

            t4 = [t for t in lista_times if t not in [t1, t2, t3]][0]
            ordem[3] = t4
            col2.markdown(f"<p style='margin-top:28px;font-size:13px;color:#94a3b8;'>❌ 4º: {t4}</p>",
                          unsafe_allow_html=True)
            dados_usuario["classificacao"][nome_grupo] = [t1, t2, t3, t4]
            palpites_grupos[nome_grupo] = [t1, t2, t3, t4]

        jogos_com_placar = _jogos_do_grupo(nome_grupo, apenas_com_placar=True)
        if jogos_com_placar:
            atual = api_data["classificacao_real"].get(nome_grupo, lista_times)
            ordem_atual = " &nbsp;|&nbsp; ".join(
                f"{pos + 1}º {time}" for pos, time in enumerate(atual)
            )
            linhas_resultados = "".join(
                f'<div class="real-line">⚽ {_formatar_placar(jogo)} '
                f'<span style="color:#94a3b8;">({jogo.get("fonte_resultado", api_data["fonte"])})</span></div>'
                for jogo in jogos_com_placar
            )
            st.markdown(f"""
            <div class="real-box">
                <div class="real-title">Classificação atual</div>
                <div class="real-line">{ordem_atual}</div>
                {linhas_resultados}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="real-box">
                <div class="real-title">Classificação atual</div>
                <div class="real-line">Aguardando resultados com placar.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Jogos do Brasil ──────────────────────────────────────────────────────
    st.markdown("## 🇧🇷 Jogos do Brasil — Grupo C")

    palpites_gols = list(dados_usuario["placar_brasil"])

    for idx, jogo_info in enumerate(JOGOS_BRASIL):
        st.markdown(f'<div class="group-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="group-header-br">🗓 {jogo_info["jogo"]} — {jogo_info["data"]} {jogo_info["hora"]}</div>',
                    unsafe_allow_html=True)
        st.caption(f"📍 {jogo_info['loc']}")

        b = idx * 2
        
        # Determina fonte do resultado (API vs Manual)
        gols_api = api_data.get("gols_brasil", [None] * 6)
        tem_resultado_api = gols_api[b] is not None and gols_api[b + 1] is not None
        jogo_finalizado_api = False
        for jogo in api_data.get("jogos_reais", []):
            if jogo_info["jogo"] in jogo["jogo"] and jogo.get("status") == "FINISHED":
                jogo_finalizado_api = True
                break
        
        badge_fonte = ""
        if tem_resultado_api and jogo_finalizado_api:
            badge_fonte = '<span style="color:#15803d; font-size:11px; font-weight:600;">✅ Football-Data.org</span>'
        else:
            resultados_manuais = _resultados_manuais()
            manual = resultados_manuais.get(jogo_info["jogo"], {})
            if manual.get("placar_c") is not None:
                badge_fonte = '<span style="color:#ca8a04; font-size:11px; font-weight:600;">✏️ Preenchimento manual</span>'

        if travado_ou_view:
            if dados_usuario["travado"]:
                g_br_salvo  = int(dados_usuario["placar_brasil"][b])
                g_adv_salvo = int(dados_usuario["placar_brasil"][b + 1])
                st.markdown(
                    f"<div style='text-align:center; font-size:22px; font-weight:800; "
                    f"color:#15803d; padding: 8px 0;'>"
                    f"🇧🇷 Brasil {g_br_salvo} × {g_adv_salvo} Adversário</div>",
                    unsafe_allow_html=True
                )
                palpites_gols[b]     = g_br_salvo
                palpites_gols[b + 1] = g_adv_salvo
            else:
                st.markdown(
                    "<span style='color:#94a3b8;font-size:13px;'>"
                    "🔒 Faça login para ver e editar seus palpites de placar</span>",
                    unsafe_allow_html=True
                )
        else:
            c1, c2 = st.columns(2)
            g_br  = c1.number_input("Gols Brasil", min_value=0, max_value=20,
                                    value=int(dados_usuario["placar_brasil"][b]),
                                    step=1, key=f"gbr_{idx}")
            g_adv = c2.number_input("Gols Adversário", min_value=0, max_value=20,
                                    value=int(dados_usuario["placar_brasil"][b + 1]),
                                    step=1, key=f"gadv_{idx}")
            palpites_gols[b]     = g_br
            palpites_gols[b + 1] = g_adv

        # ── Resultado real via API (igual ao "real-box" dos grupos) ──────────
        r_br  = api_data.get("gols_brasil", [None]*6)[b]
        r_adv = api_data.get("gols_brasil", [None]*6)[b + 1]

        # Descobre o nome do adversário a partir do jogo
        t_c, t_f = _partes_jogo(jogo_info["jogo"])
        adversario = t_f if t_c == "Brasil" else t_c

        if r_br is not None and r_adv is not None:
            if t_c == "Brasil":
                placar_str = f"Brasil {r_br} × {r_adv} {adversario}"
            else:
                placar_str = f"{adversario} {r_adv} × {r_br} Brasil"

            fonte_str = ""
            if badge_fonte:
                fonte_str = badge_fonte
            else:
                fonte_str = f'<span style="color:#94a3b8;font-size:11px;">{api_data["fonte"]}</span>'

            st.markdown(f"""
            <div class="real-box">
                <div class="real-title">Resultado real</div>
                <div class="real-line">⚽ {placar_str} {fonte_str}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="real-box">
                <div class="real-title">Resultado real</div>
                <div class="real-line">Aguardando resultado.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Botão de Trava — só aparece se autenticado e ainda não travou ────────
    if autenticado and not dados_usuario["travado"]:
        st.write("---")

        chave_trava = f"disparar_trava_{usuario_selecionado}"
        if chave_trava not in st.session_state:
            st.session_state[chave_trava] = False

        if not st.session_state[chave_trava]:
            if st.button("🚨 Salvar palpites definitivos", key="btn_salvar"):
                st.session_state[chave_trava] = True
                st.rerun()
        else:
            st.markdown("""
            <div class="cuzao-box">
                <p class="cuzao-title">⚠️ Tem certeza, cuzão?</p>
                <p class="cuzao-sub">Depois disso não dá pra editar mais nada. Juro.</p>
            </div>
            """, unsafe_allow_html=True)

            col_sim, col_nao = st.columns(2)
            if col_sim.button("🔥 Sim, quero travar!", key="btn_sim"):
                # Dupla verificação: re-lê o banco antes de gravar
                banco_atual = carregar_banco()
                if banco_atual[usuario_selecionado]["travado"]:
                    st.warning("Seus palpites já estavam travados. Nenhuma alteração feita.")
                else:
                    banco_atual[usuario_selecionado]["classificacao"] = {
                        g: list(palpites_grupos.get(g, v))
                        for g, v in GRUPOS_CONFIG.items()
                    }
                    banco_atual[usuario_selecionado]["placar_brasil"] = palpites_gols
                    banco_atual[usuario_selecionado]["travado"]       = True
                    ok = salvar_banco(banco_atual)
                    if ok:
                        st.success("✅ Palpites travados com sucesso! Boa sorte! 🍀")
                    else:
                        st.error("Falha ao salvar. Tente novamente.")
                st.session_state[chave_trava] = False
                st.rerun()

            if col_nao.button("❌ Não, quero revisar", key="btn_nao"):
                st.session_state[chave_trava] = False
                st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# ABA 2: MATA-MATA
# ──────────────────────────────────────────────────────────────────────────────
with aba_matamata:
    st.markdown("## 🌳 Chaveamento do Mata-Mata")

    if not MATA_MATA_LIBERADO:
        st.info("🔒 Esta aba ficará disponível após o encerramento da fase de grupos e a definição oficial do chaveamento real da Copa 2026.")
        st.markdown("### Prévia dos confrontos (baseado no chaveamento fixo)")

    col_mm1, col_mm2 = st.columns(2)
    for i, conf in enumerate(MATA_MATA_CONFRONTOS):
        col = col_mm1 if i % 2 == 0 else col_mm2
        with col:
            st.markdown(f'<div class="mm-card"><div class="mm-id">Confronto {conf["id"]}</div>'
                        f'<div class="mm-times">{conf["t1"]} vs {conf["t2"]}</div></div>',
                        unsafe_allow_html=True)

            vencedor_atual = dados_usuario["vencedores_mata_mata"].get(conf["id"], "")
            opcoes_mm = ["— escolher —", conf["t1"], conf["t2"]]
            idx_atual  = opcoes_mm.index(vencedor_atual) if vencedor_atual in opcoes_mm else 0

            st.radio(
                "Quem avança?",
                options=opcoes_mm,
                index=idx_atual,
                key=f"mm_{conf['id']}",
                disabled=(not MATA_MATA_LIBERADO) or dados_usuario["travado"] or modo_view_only,
                label_visibility="collapsed"
            )

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

    datas = []
    for j in jogos_exibir:
        if j["data"] not in datas:
            datas.append(j["data"])

    for data in datas:
        st.markdown(f'<div class="data-header">📆 {data}</div>', unsafe_allow_html=True)
        jogos_data = [j for j in jogos_exibir if j["data"] == data]
        for j in jogos_data:
            jogo_real = _buscar_jogo_real(j["jogo"])
            status = _status_jogo(j["data"], j["hora"])
            if jogo_real:
                if jogo_real.get("status") == "FINISHED":
                    status = "finalizado"
                elif jogo_real.get("status") == "IN_PLAY":
                    status = "aovivo"
            nome_jogo = _formatar_placar(jogo_real) if jogo_real and _tem_placar(jogo_real) else j["jogo"]
            fonte_resultado = ""
            if jogo_real and _tem_placar(jogo_real):
                fonte_resultado = f' · Resultado: {jogo_real.get("fonte_resultado", api_data["fonte"])}'
            brasil_class = "jogo-brasil" if j["brasil"] else ""
            if status == "finalizado":
                badge = '<span class="badge-finalizado">✓ Finalizado</span>'
            elif status == "aovivo":
                badge = '<span class="badge-aovivo">🔴 Ao vivo</span>'
            else:
                badge = '<span class="badge-previsto">Previsto</span>'

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
            <div class="regra-item">🥇 1º colocado correto no grupo: <strong>+2 pts</strong></div>
            <div class="regra-item">🥈 2º colocado correto no grupo: <strong>+2 pts</strong></div>
            <div class="regra-item">⚽ Placar exato do Brasil: <strong>+5 pts</strong></div>
            <div class="regra-item">✅ Vencedor/empate correto (Brasil): <strong>+3 pts</strong></div>
            <div class="regra-item">🔒 Palpite não travado: <strong>0 pts</strong> (até travar)</div>
        </div>
        """, unsafe_allow_html=True)

    linhas = []
    qualquer_jogo_realizado = any(j.get("status") == "FINISHED" for j in api_data.get("jogos_reais", []))

    for amigo in AMIGOS:
        user   = st.session_state.banco[amigo]
        total, detalhes = _calcular_pontuacao(amigo)
        travado = user["travado"]

        badges = []
        if travado:
            acertou_placar = any(
                user["placar_brasil"][i * 2]     == api_data["gols_brasil"][i * 2] and
                user["placar_brasil"][i * 2 + 1] == api_data["gols_brasil"][i * 2 + 1] and
                api_data["gols_brasil"][i * 2] is not None
                for i in range(3)
            )
            errou_tudo = qualquer_jogo_realizado and total == 0

            if acertou_placar:
                badges.append("🔮 Profeta")
            if errou_tudo:
                badges.append("🤡 Zica")

        linhas.append({
            "amigo":    amigo,
            "total":    total,
            "travado":  travado,
            "badges":   badges,
            "detalhes": detalhes,
        })

    linhas.sort(key=lambda x: (-int(x["travado"]), -x["total"]))

    if len(linhas) > 0:
        travados_com_pts = [l for l in linhas if l["travado"] and l["total"] > 0]
        if travados_com_pts:
            linhas[0]["badges"].insert(0, "👑 Líder")
            if len(travados_com_pts) > 1:
                linhas[-1]["badges"].append("🔦 Lanterna")

    posicao_icons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣"]

    for i, linha in enumerate(linhas):
        cor_borda = ""
        if i == 0 and linha["total"] > 0:
            cor_borda = "border: 2px solid #1d4ed8;"

        badge_str  = " | ".join(linha["badges"]) if linha["badges"] else ("⏳ Aguardando início" if not qualquer_jogo_realizado else "🏃 Em jogo")
        status_str = "🔒 Travado" if linha["travado"] else "🔓 Editando"
        pts_color  = "#1e3a5f" if linha["total"] > 0 else "#94a3b8"

        st.markdown(f"""
        <div class="rank-row" style="{cor_borda}">
            <div class="rank-pos">{posicao_icons[i]}</div>
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
        st.info("⏳ A pontuação começa a ser calculada após o primeiro jogo da Copa.")

    st.markdown("---")
    st.markdown("### Detalhamento por amigo")
    for linha in linhas:
        if linha["travado"] and linha["detalhes"]:
            with st.expander(f"{linha['amigo']} — {linha['total']} pts"):
                for detalhe in linha["detalhes"]:
                    status = detalhe.get("status", "wait")
                    if status == "ok":
                        icon, cls = "✅", "detail-ok"
                    elif status == "err":
                        icon, cls = "❌", "detail-err"
                    else:
                        icon, cls = "⏳", "detail-wait"
                    st.markdown(
                        f'{icon} <strong>{detalhe["cat"]}</strong> — {detalhe["texto"]} '
                        f'<span class="{cls}">+{detalhe["pts"]} pts</span>',
                        unsafe_allow_html=True
                    )
        elif not linha["travado"]:
            with st.expander(f"{linha['amigo']} — palpite em aberto"):
                st.caption("Ainda não travou os palpites.")
