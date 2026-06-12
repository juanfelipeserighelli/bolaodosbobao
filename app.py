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

# Fuso horário de Brasília (BRT = UTC-3)
BRT = timezone(timedelta(hours=-3))

st.markdown("""
<style>
.main .block-container {
    padding-top: 0.75rem; padding-bottom: 3rem;
    padding-left: 12px; padding-right: 12px; max-width: 680px;
}
h1 { font-size: 22px !important; font-weight: 800 !important; text-align: center;
     letter-spacing: -0.5px; color: #1e3a5f !important; margin-bottom: 2px !important; }
h2 { font-size: 16px !important; font-weight: 700 !important; color: #1e3a5f !important;
     margin-top: 18px !important; margin-bottom: 6px !important; }
h3 { font-size: 14px !important; font-weight: 600 !important; color: #334155 !important; }
.stTabs [data-baseweb="tab-list"] { gap: 3px; background: #f1f5f9; padding: 4px; border-radius: 10px; }
.stTabs [data-baseweb="tab"] {
    font-size: 12px !important; font-weight: 600 !important;
    padding: 7px 10px !important; border-radius: 7px !important;
    background: transparent !important; color: #64748b !important; border: none !important;
}
.stTabs [aria-selected="true"] { background: #1e3a5f !important; color: #ffffff !important; }
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
.status-travado {
    background: #dcfce7; border-left: 4px solid #16a34a;
    padding: 10px 14px; border-radius: 8px; color: #14532d;
    font-weight: 700; font-size: 13px; text-align: center; margin-bottom: 14px;
}
.status-editando {
    background: #fef9c3; border-left: 4px solid #ca8a04;
    padding: 10px 14px; border-radius: 8px; color: #713f12;
    font-weight: 600; font-size: 13px; margin-bottom: 14px;
}
.cuzao-box {
    background: #fff1f2; border: 2px solid #e11d48;
    padding: 16px; border-radius: 12px; text-align: center; margin: 12px 0;
}
.cuzao-title { color: #be123c !important; font-weight: 700 !important;
               font-size: 15px !important; margin: 0 0 6px !important; }
.cuzao-sub   { color: #3f3f46; font-size: 13px; font-weight: 500; margin: 0; }
.jogo-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 10px 13px; margin-bottom: 8px;
    display: flex; align-items: center; gap: 10px;
}
.jogo-data  { font-size: 11px; color: #64748b; min-width: 36px; text-align: center; }
.jogo-hora  { font-size: 11px; font-weight: 700; color: #334155; min-width: 34px; }
.jogo-nome  { font-size: 13px; font-weight: 600; color: #1e293b; flex: 1; }
.jogo-local { font-size: 11px; color: #94a3b8; }
.badge-finalizado { background: #dcfce7; color: #15803d; font-size: 10px;
    font-weight: 700; padding: 2px 7px; border-radius: 20px; white-space: nowrap; }
.badge-aovivo { background: #fef2f2; color: #dc2626; font-size: 10px;
    font-weight: 700; padding: 2px 7px; border-radius: 20px; white-space: nowrap;
    animation: pulse-badge 1.5s ease-in-out infinite; }
.badge-previsto { background: #f1f5f9; color: #64748b; font-size: 10px;
    font-weight: 600; padding: 2px 7px; border-radius: 20px; white-space: nowrap; }
@keyframes pulse-badge { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
.data-header {
    font-size: 12px; font-weight: 700; color: #475569;
    background: #f8fafc; padding: 5px 12px; border-radius: 6px;
    margin: 10px 0 6px; border-left: 3px solid #1e3a5f;
}
.jogo-brasil { border-left: 3px solid #15803d !important; }
.countdown-box {
    background: linear-gradient(135deg, #1e3a5f 0%, #1d4ed8 100%);
    color: white; border-radius: 12px; padding: 12px 16px;
    text-align: center; margin-bottom: 16px;
}
.countdown-label { font-size: 11px; font-weight: 600; opacity: 0.8;
    text-transform: uppercase; letter-spacing: 0.05em; }
.countdown-time  { font-size: 22px; font-weight: 800; letter-spacing: 1px; }
.countdown-game  { font-size: 12px; opacity: 0.85; margin-top: 2px; }
.rank-row {
    display: flex; align-items: center; gap: 10px;
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 10px 13px; margin-bottom: 7px;
}
.rank-pos   { font-size: 18px; font-weight: 800; min-width: 28px; color: #1e3a5f; }
.rank-nome  { font-size: 14px; font-weight: 700; color: #1e293b; flex: 1; }
.rank-pts   { font-size: 20px; font-weight: 800; color: #1e3a5f; min-width: 40px; text-align: right; }
.rank-pts-label { font-size: 10px; color: #94a3b8; text-align: right; }
.rank-badges { font-size: 12px; color: #64748b; }
.rank-status-open { color: #ca8a04; font-size: 11px; font-weight: 600; }
.rank-status-lock { color: #16a34a; font-size: 11px; font-weight: 600; }
.view-banner {
    background: #eff6ff; border: 1px solid #bfdbfe;
    border-radius: 8px; padding: 9px 14px; font-size: 13px;
    color: #1d4ed8; font-weight: 600; margin-bottom: 14px; text-align: center;
}
.mm-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 11px 14px; margin-bottom: 8px;
}
.mm-id     { font-size: 10px; color: #94a3b8; font-weight: 600;
    text-transform: uppercase; margin-bottom: 4px; }
.mm-times  { font-size: 13px; font-weight: 600; color: #334155; }
.fonte-dados {
    font-size: 11px; color: #94a3b8; text-align: right;
    margin-bottom: 4px; font-style: italic;
}
.stNumberInput input { font-size: 16px !important; text-align: center !important; }
.stButton > button { width: 100%; border-radius: 8px; height: 2.8rem;
    font-weight: 700; font-size: 14px; }
.stSelectbox label { font-size: 13px !important; }
.regra-box {
    background: #f0f9ff; border: 1px solid #bae6fd;
    border-radius: 10px; padding: 12px 14px; margin-bottom: 14px;
}
.regra-item { font-size: 13px; color: #0c4a6e; padding: 3px 0; }
.api-status-ok  { background: #dcfce7; color: #15803d; font-size: 11px; font-weight: 600;
    padding: 3px 8px; border-radius: 6px; display: inline-block; }
.api-status-err { background: #fef2f2; color: #dc2626; font-size: 11px; font-weight: 600;
    padding: 3px 8px; border-radius: 6px; display: inline-block; }
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
    {"rodada": 1, "jogo": "Brasil x Marrocos", "data": "13/06", "hora_brt": "19:00", "loc": "Nova York/NJ"},
    {"rodada": 2, "jogo": "Brasil x Haiti",     "data": "19/06", "hora_brt": "21:30", "loc": "Filadélfia"},
    {"rodada": 3, "jogo": "Escócia x Brasil",   "data": "24/06", "hora_brt": "19:00", "loc": "Miami"},
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

MATA_MATA_LIBERADO = False

# Próximo jogo do Brasil — em BRT (aware)
PROXIMO_JOGO_BRASIL = {
    "nome":      "Brasil x Marrocos",
    "data_hora": datetime(2026, 6, 13, 19, 0, 0, tzinfo=BRT),
}

# ==============================================================================
# CALENDÁRIO FIXO — horários em BRT
# ==============================================================================
CALENDARIO_FIXO = [
    {"data": "11/06", "hora_brt": "16:00", "jogo": "México x África do Sul",      "local": "Cidade do México", "brasil": False},
    {"data": "11/06", "hora_brt": "23:00", "jogo": "Tchéquia x Coreia do Sul",    "local": "Guadalajara",      "brasil": False},
    {"data": "12/06", "hora_brt": "16:00", "jogo": "Canadá x Bósnia",             "local": "Toronto",          "brasil": False},
    {"data": "12/06", "hora_brt": "22:00", "jogo": "Estados Unidos x Paraguai",   "local": "Los Angeles",      "brasil": False},
    {"data": "13/06", "hora_brt": "16:00", "jogo": "Catar x Suíça",               "local": "San Francisco",    "brasil": False},
    {"data": "13/06", "hora_brt": "19:00", "jogo": "Brasil x Marrocos",           "local": "Nova York/NJ",     "brasil": True},
    {"data": "13/06", "hora_brt": "22:00", "jogo": "Haiti x Escócia",             "local": "Boston",           "brasil": False},
    {"data": "14/06", "hora_brt": "01:00", "jogo": "Austrália x Turquia",         "local": "Vancouver",        "brasil": False},
    {"data": "14/06", "hora_brt": "14:00", "jogo": "Alemanha x Curaçao",          "local": "Houston",          "brasil": False},
    {"data": "14/06", "hora_brt": "17:00", "jogo": "Países Baixos x Japão",       "local": "Dallas",           "brasil": False},
    {"data": "14/06", "hora_brt": "20:00", "jogo": "Costa do Marfim x Equador",   "local": "Filadélfia",       "brasil": False},
    {"data": "14/06", "hora_brt": "23:00", "jogo": "Suécia x Tunísia",            "local": "Monterrey",        "brasil": False},
    {"data": "15/06", "hora_brt": "13:00", "jogo": "Espanha x Cabo Verde",        "local": "Atlanta",          "brasil": False},
    {"data": "15/06", "hora_brt": "16:00", "jogo": "Bélgica x Egito",             "local": "Seattle",          "brasil": False},
    {"data": "15/06", "hora_brt": "19:00", "jogo": "Arábia Saudita x Uruguai",    "local": "Miami",            "brasil": False},
    {"data": "15/06", "hora_brt": "22:00", "jogo": "Irã x Nova Zelândia",         "local": "Los Angeles",      "brasil": False},
    {"data": "16/06", "hora_brt": "16:00", "jogo": "França x Senegal",            "local": "Nova York/NJ",     "brasil": False},
    {"data": "16/06", "hora_brt": "19:00", "jogo": "Iraque x Noruega",            "local": "Boston",           "brasil": False},
    {"data": "16/06", "hora_brt": "22:00", "jogo": "Argentina x Argélia",         "local": "Kansas City",      "brasil": False},
    {"data": "17/06", "hora_brt": "01:00", "jogo": "Áustria x Jordânia",          "local": "San Francisco",    "brasil": False},
    {"data": "17/06", "hora_brt": "14:00", "jogo": "Portugal x RD Congo",         "local": "Houston",          "brasil": False},
    {"data": "17/06", "hora_brt": "17:00", "jogo": "Inglaterra x Croácia",        "local": "Dallas",           "brasil": False},
    {"data": "17/06", "hora_brt": "20:00", "jogo": "Gana x Panamá",               "local": "Toronto",          "brasil": False},
    {"data": "17/06", "hora_brt": "23:00", "jogo": "Uzbequistão x Colômbia",      "local": "Cidade do México", "brasil": False},
    {"data": "18/06", "hora_brt": "13:00", "jogo": "Tchéquia x África do Sul",    "local": "Atlanta",          "brasil": False},
    {"data": "18/06", "hora_brt": "16:00", "jogo": "Suíça x Bósnia",              "local": "Los Angeles",      "brasil": False},
    {"data": "18/06", "hora_brt": "19:00", "jogo": "Canadá x Catar",              "local": "Vancouver",        "brasil": False},
    {"data": "18/06", "hora_brt": "22:00", "jogo": "México x Coreia do Sul",      "local": "Guadalajara",      "brasil": False},
    {"data": "19/06", "hora_brt": "16:00", "jogo": "Estados Unidos x Austrália",  "local": "Seattle",          "brasil": False},
    {"data": "19/06", "hora_brt": "19:00", "jogo": "Escócia x Marrocos",          "local": "Boston",           "brasil": False},
    {"data": "19/06", "hora_brt": "21:30", "jogo": "Brasil x Haiti",              "local": "Filadélfia",       "brasil": True},
    {"data": "20/06", "hora_brt": "00:00", "jogo": "Turquia x Paraguai",          "local": "San Francisco",    "brasil": False},
    {"data": "20/06", "hora_brt": "14:00", "jogo": "Países Baixos x Suécia",      "local": "Houston",          "brasil": False},
    {"data": "20/06", "hora_brt": "17:00", "jogo": "Alemanha x Costa do Marfim",  "local": "Toronto",          "brasil": False},
    {"data": "20/06", "hora_brt": "21:00", "jogo": "Equador x Curaçao",           "local": "Kansas City",      "brasil": False},
    {"data": "21/06", "hora_brt": "01:00", "jogo": "Tunísia x Japão",             "local": "Monterrey",        "brasil": False},
    {"data": "21/06", "hora_brt": "13:00", "jogo": "Espanha x Arábia Saudita",    "local": "Atlanta",          "brasil": False},
    {"data": "21/06", "hora_brt": "16:00", "jogo": "Bélgica x Irã",               "local": "Los Angeles",      "brasil": False},
    {"data": "21/06", "hora_brt": "19:00", "jogo": "Uruguai x Cabo Verde",        "local": "Miami",            "brasil": False},
    {"data": "21/06", "hora_brt": "22:00", "jogo": "Nova Zelândia x Egito",       "local": "Vancouver",        "brasil": False},
    {"data": "22/06", "hora_brt": "14:00", "jogo": "Argentina x Áustria",         "local": "Dallas",           "brasil": False},
    {"data": "22/06", "hora_brt": "18:00", "jogo": "França x Iraque",             "local": "Filadélfia",       "brasil": False},
    {"data": "22/06", "hora_brt": "21:00", "jogo": "Noruega x Senegal",           "local": "Nova York/NJ",     "brasil": False},
    {"data": "23/06", "hora_brt": "00:00", "jogo": "Jordânia x Argélia",          "local": "San Francisco",    "brasil": False},
    {"data": "23/06", "hora_brt": "14:00", "jogo": "Portugal x Uzbequistão",      "local": "Houston",          "brasil": False},
    {"data": "23/06", "hora_brt": "17:00", "jogo": "Inglaterra x Gana",           "local": "Boston",           "brasil": False},
    {"data": "23/06", "hora_brt": "20:00", "jogo": "Panamá x Croácia",            "local": "Toronto",          "brasil": False},
    {"data": "23/06", "hora_brt": "23:00", "jogo": "Colômbia x RD Congo",         "local": "Guadalajara",      "brasil": False},
    {"data": "24/06", "hora_brt": "16:00", "jogo": "Suíça x Canadá",              "local": "Vancouver",        "brasil": False},
    {"data": "24/06", "hora_brt": "16:00", "jogo": "Bósnia x Catar",              "local": "Seattle",          "brasil": False},
    {"data": "24/06", "hora_brt": "19:00", "jogo": "Escócia x Brasil",            "local": "Miami",            "brasil": True},
    {"data": "24/06", "hora_brt": "19:00", "jogo": "Marrocos x Haiti",            "local": "Atlanta",          "brasil": False},
    {"data": "24/06", "hora_brt": "22:00", "jogo": "Tchéquia x México",           "local": "Cidade do México", "brasil": False},
    {"data": "24/06", "hora_brt": "22:00", "jogo": "África do Sul x Coreia",      "local": "Monterrey",        "brasil": False},
    {"data": "25/06", "hora_brt": "17:00", "jogo": "Equador x Alemanha",          "local": "Nova York/NJ",     "brasil": False},
    {"data": "25/06", "hora_brt": "17:00", "jogo": "Curaçao x Costa do Marfim",   "local": "Filadélfia",       "brasil": False},
    {"data": "25/06", "hora_brt": "20:00", "jogo": "Japão x Suécia",              "local": "Dallas",           "brasil": False},
    {"data": "25/06", "hora_brt": "20:00", "jogo": "Tunísia x Países Baixos",     "local": "Kansas City",      "brasil": False},
    {"data": "25/06", "hora_brt": "23:00", "jogo": "Turquia x Estados Unidos",    "local": "Los Angeles",      "brasil": False},
    {"data": "25/06", "hora_brt": "23:00", "jogo": "Paraguai x Austrália",        "local": "San Francisco",    "brasil": False},
    {"data": "26/06", "hora_brt": "16:00", "jogo": "Noruega x França",            "local": "Boston",           "brasil": False},
    {"data": "26/06", "hora_brt": "16:00", "jogo": "Senegal x Iraque",            "local": "Toronto",          "brasil": False},
    {"data": "26/06", "hora_brt": "21:00", "jogo": "Cabo Verde x Arábia Saudita", "local": "Houston",          "brasil": False},
    {"data": "26/06", "hora_brt": "21:00", "jogo": "Uruguai x Espanha",           "local": "Guadalajara",      "brasil": False},
    {"data": "27/06", "hora_brt": "00:00", "jogo": "Egito x Irã",                 "local": "Seattle",          "brasil": False},
    {"data": "27/06", "hora_brt": "00:00", "jogo": "Nova Zelândia x Bélgica",     "local": "Vancouver",        "brasil": False},
    {"data": "27/06", "hora_brt": "18:00", "jogo": "Panamá x Inglaterra",         "local": "Nova York/NJ",     "brasil": False},
    {"data": "27/06", "hora_brt": "18:00", "jogo": "Croácia x Gana",              "local": "Filadélfia",       "brasil": False},
    {"data": "27/06", "hora_brt": "20:30", "jogo": "Colômbia x Portugal",         "local": "Miami",            "brasil": False},
    {"data": "27/06", "hora_brt": "20:30", "jogo": "RD Congo x Uzbequistão",      "local": "Atlanta",          "brasil": False},
    {"data": "27/06", "hora_brt": "23:00", "jogo": "Argélia x Áustria",           "local": "Kansas City",      "brasil": False},
    {"data": "27/06", "hora_brt": "23:00", "jogo": "Jordânia x Argentina",        "local": "Dallas",           "brasil": False},
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
    for amigo in AMIGOS:
        banco[amigo] = {
            "travado": False,
            "classificacao": {g: list(t) for g, t in GRUPOS_CONFIG.items()},
            "placar_brasil": [0, 0, 0, 0, 0, 0],
            "vencedores_mata_mata": {c["id"]: "" for c in MATA_MATA_CONFRONTOS},
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
            for amigo in AMIGOS:
                if amigo in dados:
                    d = dados[amigo]
                    banco_seguro[amigo]["travado"]              = bool(d.get("travado", False))
                    banco_seguro[amigo]["classificacao"]        = d.get("classificacao",        banco_seguro[amigo]["classificacao"])
                    banco_seguro[amigo]["placar_brasil"]        = d.get("placar_brasil",        banco_seguro[amigo]["placar_brasil"])
                    banco_seguro[amigo]["vencedores_mata_mata"] = d.get("vencedores_mata_mata", banco_seguro[amigo]["vencedores_mata_mata"])
            return banco_seguro
        if resp.status_code in (401, 403):
            st.warning("⚠️ JSONBin: chave de API inválida.")
        elif resp.status_code == 404:
            st.warning("⚠️ JSONBin: bin não encontrado.")
    except requests.exceptions.Timeout:
        st.warning("⚠️ JSONBin sem resposta (timeout). Dados locais.")
    except Exception:
        pass
    return banco_seguro

def salvar_banco(banco_completo):
    try:
        bin_id  = st.secrets.get("JSONBIN_ID", "")
        api_key = st.secrets.get("JSONBIN_KEY", "")
        if not bin_id or not api_key:
            st.session_state.banco = banco_completo
            return True
        resp = requests.put(_jsonbin_url(), json=banco_completo, headers=_jsonbin_headers(), timeout=8)
        if resp.status_code == 200:
            st.session_state.banco = banco_completo
            return True
        else:
            st.error(f"Erro ao salvar (HTTP {resp.status_code}): {resp.text[:200]}")
    except requests.exceptions.Timeout:
        st.error("Timeout ao salvar. Tente novamente.")
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
# RESULTADOS REAIS DA API — com classificação real dos grupos
# ==============================================================================
TRADUCAO = {
    "Brazil": "Brasil", "Haiti": "Haiti", "Morocco": "Marrocos", "Scotland": "Escócia",
    "Mexico": "México", "South Africa": "África do Sul",
    "Korea Republic": "República da Coreia", "Czech Republic": "Tchéquia", "Czechia": "Tchéquia",
    "Bosnia and Herzegovina": "Bósnia e Herzegovina", "Canada": "Canadá", "Qatar": "Catar", "Switzerland": "Suíça",
    "Australia": "Austrália", "Paraguay": "Paraguai", "Turkey": "Turquia",
    "USA": "Estados Unidos", "United States": "Estados Unidos",
    "Curaçao": "Curaçao", "Ecuador": "Equador", "Germany": "Alemanha",
    "Ivory Coast": "Costa do Marfim", "Cote d'Ivoire": "Costa do Marfim",
    "Japan": "Japão", "Netherlands": "Países Baixos", "Sweden": "Suécia", "Tunisia": "Tunísia",
    "Belgium": "Bélgica", "Egypt": "Egito", "Iran": "Irã", "New Zealand": "Nova Zelândia",
    "Cape Verde": "Cabo Verde", "Saudi Arabia": "Arábia Saudita", "Spain": "Espanha", "Uruguay": "Uruguai",
    "France": "França", "Iraq": "Iraque", "Norway": "Noruega", "Senegal": "Senegal",
    "Algeria": "Argélia", "Argentina": "Argentina", "Austria": "Áustria", "Jordan": "Jordânia",
    "Colombia": "Colômbia", "DR Congo": "RD Congo", "Portugal": "Portugal", "Uzbekistan": "Uzbequistão",
    "Croatia": "Croácia", "England": "Inglaterra", "Ghana": "Gana", "Panama": "Panamá",
}

def _montar_resultado(jogos_reais, fonte, classificacao_api=None):
    """
    Constrói o dict de retorno.
    classificacao_api: dict {grupo: [t1,t2,t3,t4]} vindo da API de standings.
    Se não disponível, mantém a ordem padrão (grupos sem jogos ainda).
    """
    # Começa com ordem padrão
    class_real = {g: list(t) for g, t in GRUPOS_CONFIG.items()}

    # Sobrescreve apenas os grupos onde a API retornou standings reais
    if classificacao_api:
        for grupo, ordem in classificacao_api.items():
            if grupo in class_real and len(ordem) >= 2:
                class_real[grupo] = ordem

    # Gols do Brasil
    gols_brasil = [None, None, None, None, None, None]
    idx_br = 0
    for j in jogos_reais:
        if j["status"] == "FINISHED" and idx_br < 3:
            nome = j["jogo"]
            gc, gf = j["placar_c"], j["placar_f"]
            if nome.startswith("Brasil"):
                gols_brasil[idx_br * 2]     = gc
                gols_brasil[idx_br * 2 + 1] = gf
                idx_br += 1
            elif " x Brasil" in nome or nome.endswith("Brasil"):
                gols_brasil[idx_br * 2]     = gf
                gols_brasil[idx_br * 2 + 1] = gc
                idx_br += 1

    return {
        "fonte":              fonte,
        "classificacao_real": class_real,
        "jogos_reais":        jogos_reais,
        "gols_brasil":        gols_brasil,
    }

@st.cache_data(ttl=600)
def obter_resultados():
    """
    Tenta as 3 APIs em sequência.
    API 1 (football-data.org): também busca standings reais dos grupos.
    """
    padrao = {
        "fonte":              "calendário fixo",
        "classificacao_real": {g: list(t) for g, t in GRUPOS_CONFIG.items()},
        "jogos_reais":        [],
        "gols_brasil":        [None, None, None, None, None, None],
    }

    # ── API 1: football-data.org ──────────────────────────────────────────────
    try:
        token = st.secrets.get("FOOTBALL_DATA_TOKEN", "")
        if token:
            headers = {"X-Auth-Token": token}

            # 1a. Busca partidas
            r_matches = requests.get(
                "https://api.football-data.org/v4/competitions/WC/matches?season=2026",
                headers=headers, timeout=6
            )
            # 1b. Busca standings (classificação real dos grupos)
            r_stands = requests.get(
                "https://api.football-data.org/v4/competitions/WC/standings?season=2026",
                headers=headers, timeout=6
            )

            if r_matches.status_code == 200:
                matches = r_matches.json().get("matches", [])
                jogos = []
                for m in matches:
                    t_c    = TRADUCAO.get(m["homeTeam"]["name"], m["homeTeam"]["name"])
                    t_f    = TRADUCAO.get(m["awayTeam"]["name"], m["awayTeam"]["name"])
                    sc     = m.get("score", {}).get("fullTime", {})
                    status = m.get("status", "SCHEDULED")
                    jogos.append({
                        "jogo":     f"{t_c} x {t_f}",
                        "placar_c": sc.get("home"),
                        "placar_f": sc.get("away"),
                        "status":   "FINISHED" if status == "FINISHED" else status,
                    })

                # Processa standings se disponível
                class_api = {}
                if r_stands.status_code == 200:
                    standings_data = r_stands.json().get("standings", [])
                    for grupo_data in standings_data:
                        grupo_nome = grupo_data.get("group", "")
                        # Mapeia "Group A" → "Grupo A"
                        grupo_pt = grupo_nome.replace("Group ", "Grupo ")
                        tabela   = grupo_data.get("table", [])
                        if tabela:
                            class_api[grupo_pt] = [
                                TRADUCAO.get(row["team"]["name"], row["team"]["name"])
                                for row in tabela
                            ]

                if jogos:
                    return _montar_resultado(jogos, "football-data.org ✓", class_api or None)
    except Exception:
        pass

    # ── API 2: Zafronix ───────────────────────────────────────────────────────
    try:
        token_z = st.secrets.get("ZAFRONIX_KEY", "zwc_free_85be12c14621f2117b7dae7f")
        r = requests.get(
            "https://api.zafronix.com/fifa/worldcup/v1/tournaments/2026/fixtures",
            headers={"X-API-Key": token_z}, timeout=5
        )
        if r.status_code == 200:
            fixtures = r.json().get("fixtures", [])
            if fixtures:
                jogos = []
                for m in fixtures:
                    t_c = TRADUCAO.get(m.get("home_team", ""), m.get("home_team", ""))
                    t_f = TRADUCAO.get(m.get("away_team", ""), m.get("away_team", ""))
                    st_ = m.get("status", "SCHEDULED")
                    jogos.append({
                        "jogo":     f"{t_c} x {t_f}",
                        "placar_c": m.get("home_score"),
                        "placar_f": m.get("away_score"),
                        "status":   "FINISHED" if st_ == "FINISHED" else st_,
                    })
                return _montar_resultado(jogos, "Zafronix ✓")
    except Exception:
        pass

    # ── API 3: Sportmonks ─────────────────────────────────────────────────────
    try:
        token_sm = st.secrets.get("SPORTMONKS_TOKEN", "")
        if token_sm:
            r = requests.get(
                f"https://api.sportmonks.com/v3/football/fixtures?api_token={token_sm}&include=participants,scores",
                timeout=5
            )
            if r.status_code == 200:
                fixtures = r.json().get("data", [])
                jogos = []
                for m in fixtures:
                    parts = m.get("participants", [])
                    if len(parts) < 2:
                        continue
                    t_c = TRADUCAO.get(parts[0].get("name", ""), parts[0].get("name", ""))
                    t_f = TRADUCAO.get(parts[1].get("name", ""), parts[1].get("name", ""))
                    sc  = m.get("scores", {})
                    st_ = m.get("state", {})
                    sn  = st_.get("name", "") if isinstance(st_, dict) else str(st_)
                    jogos.append({
                        "jogo":     f"{t_c} x {t_f}",
                        "placar_c": sc.get("localteam_score"),
                        "placar_f": sc.get("visitorteam_score"),
                        "status":   "FINISHED" if sn in ("FT", "ENDED", "AET", "PEN") else "SCHEDULED",
                    })
                if jogos:
                    return _montar_resultado(jogos, "Sportmonks ✓")
    except Exception:
        pass

    return padrao

api_data = obter_resultados()

# ==============================================================================
# HELPERS — TODOS TIMEZONE-AWARE EM BRT
# ==============================================================================
def _dt_jogo_brt(data_str: str, hora_str: str) -> datetime:
    """
    Converte data 'DD/MM' e hora 'HH:MM' (BRT) em datetime aware (BRT).
    Retorna None se o parse falhar.
    """
    try:
        dia, mes = data_str.split("/")
        hora_limpa = hora_str.strip()
        return datetime(2026, int(mes), int(dia),
                        int(hora_limpa[:2]), int(hora_limpa[3:5]),
                        tzinfo=BRT)
    except Exception:
        return None

def _status_jogo(data_str: str, hora_str: str) -> str:
    """
    Retorna 'finalizado', 'aovivo' ou 'previsto'.
    Compara em BRT para exibição correta no Brasil.
    """
    dt = _dt_jogo_brt(data_str, hora_str)
    if dt is None:
        return "previsto"
    now_brt = datetime.now(BRT)
    delta_min = (now_brt - dt).total_seconds() / 60
    if delta_min > 110:   # jogo terminou (partida dura ~110 min)
        return "finalizado"
    if 0 <= delta_min <= 110:
        return "aovivo"
    return "previsto"

def _hora_display(hora_str: str) -> str:
    """Formata '16:00' → '16h00' para exibição."""
    return hora_str.replace(":", "h")

def _countdown_brasil():
    """Retorna (tempo_str, nome_jogo) ou None se o próximo jogo já passou."""
    agora = datetime.now(BRT)
    alvo  = PROXIMO_JOGO_BRASIL["data_hora"]
    delta = alvo - agora
    if delta.total_seconds() <= 0:
        return None
    total_min = int(delta.total_seconds() // 60)
    dias      = total_min // (60 * 24)
    horas_r   = (total_min % (60 * 24)) // 60
    minutos   = total_min % 60
    if dias > 0:
        return f"{dias}d {horas_r:02d}h {minutos:02d}min", PROXIMO_JOGO_BRASIL["nome"]
    return f"{horas_r:02d}h {minutos:02d}min", PROXIMO_JOGO_BRASIL["nome"]

def _grupos_com_resultado():
    """
    Retorna set de grupos com ao menos 1 jogo FINISHED na API.
    Também aceita o status calculado pelo calendário fixo (para quando a API falha).
    """
    finalizados = set()
    jogos_reais = api_data.get("jogos_reais", [])

    if jogos_reais:
        # Usa dados da API
        for nome_grupo, times in GRUPOS_CONFIG.items():
            for jogo in jogos_reais:
                if jogo.get("status") != "FINISHED":
                    continue
                partes = jogo["jogo"].replace(" x ", "|").split("|")
                t_c = partes[0].strip() if partes else ""
                t_f = partes[1].strip() if len(partes) > 1 else ""
                if t_c in times or t_f in times:
                    finalizados.add(nome_grupo)
                    break
    else:
        # Fallback: usa o calendário fixo + horário atual BRT
        for nome_grupo, times in GRUPOS_CONFIG.items():
            for jogo_cal in CALENDARIO_FIXO:
                status = _status_jogo(jogo_cal["data"], jogo_cal["hora_brt"])
                if status != "finalizado":
                    continue
                partes = jogo_cal["jogo"].replace(" x ", "|").split("|")
                t_c = partes[0].strip() if partes else ""
                t_f = partes[1].strip() if len(partes) > 1 else ""
                if t_c in times or t_f in times:
                    finalizados.add(nome_grupo)
                    break

    return finalizados

def _calcular_pontuacao(amigo):
    """Calcula pontuação. Retorna (total, detalhes_lista)."""
    user  = st.session_state.banco[amigo]
    real  = api_data
    total = 0
    det   = []

    if not user["travado"]:
        return 0, []

    grupos_ativos = _grupos_com_resultado()

    # Fase de grupos — 2 pts por posição (1º e 2º corretos)
    pts_g = 0
    for g in GRUPOS_CONFIG:
        if g not in grupos_ativos:
            continue
        if user["classificacao"][g][0] == real["classificacao_real"][g][0]:
            pts_g += 2
        if user["classificacao"][g][1] == real["classificacao_real"][g][1]:
            pts_g += 2
    total += pts_g
    det.append(("Fase de grupos", pts_g))

    # Jogos do Brasil — 5 pts placar exato, 3 pts resultado correto
    pts_br = 0
    for i in range(3):
        b     = i * 2
        p_br  = user["placar_brasil"][b]
        p_adv = user["placar_brasil"][b + 1]
        r_br  = real["gols_brasil"][b]
        r_adv = real["gols_brasil"][b + 1]
        if r_br is None or r_adv is None:
            continue
        if p_br == r_br and p_adv == r_adv:
            pts_br += 5
        elif (
            (p_br > p_adv and r_br > r_adv) or
            (p_br < p_adv and r_br < r_adv) or
            (p_br == p_adv and r_br == r_adv)
        ):
            pts_br += 3
    total += pts_br
    det.append(("Jogos do Brasil", pts_br))

    return total, det

# ==============================================================================
# CABEÇALHO
# ==============================================================================
st.markdown("# 🏆 Bolão do Bobão — Copa 2026")

result_cd = _countdown_brasil()
if result_cd:
    tempo_str, nome_jogo = result_cd
    st.markdown(f"""
    <div class="countdown-box">
        <div class="countdown-label">⏱ Próximo jogo do Brasil (horário de Brasília)</div>
        <div class="countdown-time">{tempo_str}</div>
        <div class="countdown-game">{nome_jogo} — trave seus palpites antes!</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# SELEÇÃO DE USUÁRIO + PIN
# ==============================================================================
col_sel, col_pin = st.columns([2, 1])
with col_sel:
    usuario_selecionado = st.selectbox("👤 Quem é você?", AMIGOS, key="selectbox_usuario")

if "ultimo_usuario" not in st.session_state:
    st.session_state.ultimo_usuario = usuario_selecionado
if st.session_state.ultimo_usuario != usuario_selecionado:
    st.session_state.usuario_autenticado = None
    st.session_state.tentativas_pin      = 0
    st.session_state.ultimo_usuario      = usuario_selecionado

dados_usuario  = st.session_state.banco[usuario_selecionado]
autenticado    = (st.session_state.usuario_autenticado == usuario_selecionado)
modo_view_only = not autenticado

with col_pin:
    if not autenticado:
        pin_input = st.text_input("🔑 PIN", type="password", max_chars=6,
                                   placeholder="••••", key=f"pin_{usuario_selecionado}")
        if pin_input:
            if pin_input == PINS[usuario_selecionado]:
                banco_fresco = carregar_banco()
                st.session_state.banco         = banco_fresco
                dados_usuario                  = st.session_state.banco[usuario_selecionado]
                st.session_state.usuario_autenticado = usuario_selecionado
                st.session_state.tentativas_pin      = 0
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
        st.markdown('<div class="status-travado">🔒 Palpites travados! Boa sorte, cuzão! 🍀</div>',
                    unsafe_allow_html=True)
    elif autenticado and not dados_usuario["travado"]:
        st.markdown('<div class="status-editando">✏️ Editando — defina os grupos e trave antes do 1º jogo!</div>',
                    unsafe_allow_html=True)
    elif not autenticado and dados_usuario["travado"]:
        st.markdown('<div class="status-travado">🔒 Palpites travados — visualizando como convidado.</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="view-banner">👁 Modo visualização — faça login com seu PIN para editar</div>',
                    unsafe_allow_html=True)

    travado_ou_view = dados_usuario["travado"] or modo_view_only
    palpites_grupos = {}

    st.markdown("## 📊 Classificação dos Grupos")

    for nome_grupo, lista_times in GRUPOS_CONFIG.items():
        st.markdown('<div class="group-card">', unsafe_allow_html=True)
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
                st.markdown("<span style='color:#94a3b8;font-size:13px;'>"
                            "🔒 Faça login para ver e editar</span>",
                            unsafe_allow_html=True)
            palpites_grupos[nome_grupo] = ordem
        else:
            col1, col2 = st.columns(2)
            t1 = col1.selectbox("🥇 1º", lista_times,
                                index=lista_times.index(ordem[0]),
                                key=f"t1_{nome_grupo}")
            if t1 != ordem[0]:
                idx = ordem.index(t1)
                ordem[idx] = ordem[0]; ordem[0] = t1
                dados_usuario["classificacao"][nome_grupo] = ordem
                st.rerun()

            opcoes_2 = [t for t in lista_times if t != t1]
            t2 = col2.selectbox("🥈 2º", opcoes_2,
                                index=opcoes_2.index(ordem[1]) if ordem[1] in opcoes_2 else 0,
                                key=f"t2_{nome_grupo}")
            if t2 != ordem[1]:
                idx = ordem.index(t2)
                ordem[idx] = ordem[1]; ordem[1] = t2
                dados_usuario["classificacao"][nome_grupo] = ordem
                st.rerun()

            opcoes_3 = [t for t in lista_times if t != t1 and t != t2]
            t3 = col1.selectbox("🥉 3º", opcoes_3,
                                index=opcoes_3.index(ordem[2]) if ordem[2] in opcoes_3 else 0,
                                key=f"t3_{nome_grupo}")
            if t3 != ordem[2]:
                idx = ordem.index(t3)
                ordem[idx] = ordem[2]; ordem[2] = t3
                dados_usuario["classificacao"][nome_grupo] = ordem
                st.rerun()

            t4 = [t for t in lista_times if t not in [t1, t2, t3]][0]
            ordem[3] = t4
            col2.markdown(f"<p style='margin-top:28px;font-size:13px;color:#94a3b8;'>❌ 4º: {t4}</p>",
                          unsafe_allow_html=True)
            dados_usuario["classificacao"][nome_grupo] = [t1, t2, t3, t4]
            palpites_grupos[nome_grupo] = [t1, t2, t3, t4]

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Jogos do Brasil ───────────────────────────────────────────────────────
    st.markdown("## 🇧🇷 Jogos do Brasil — Grupo C")
    palpites_gols = list(dados_usuario["placar_brasil"])

    for idx, jogo_info in enumerate(JOGOS_BRASIL):
        st.markdown('<div class="group-card">', unsafe_allow_html=True)
        hora_d = _hora_display(jogo_info["hora_brt"])
        st.markdown(f'<div class="group-header-br">🗓 {jogo_info["jogo"]} — {jogo_info["data"]} {hora_d} (BRT)</div>',
                    unsafe_allow_html=True)
        st.caption(f"📍 {jogo_info['loc']}")
        b = idx * 2

        if travado_ou_view:
            if dados_usuario["travado"]:
                g_br  = int(dados_usuario["placar_brasil"][b])
                g_adv = int(dados_usuario["placar_brasil"][b + 1])
                st.markdown(
                    f"<div style='text-align:center;font-size:22px;font-weight:800;"
                    f"color:#15803d;padding:8px 0;'>🇧🇷 Brasil {g_br} × {g_adv} Adversário</div>",
                    unsafe_allow_html=True
                )
                palpites_gols[b] = g_br; palpites_gols[b + 1] = g_adv
            else:
                st.markdown("<span style='color:#94a3b8;font-size:13px;'>"
                            "🔒 Faça login para ver e editar o placar</span>",
                            unsafe_allow_html=True)
        else:
            c1, c2 = st.columns(2)
            g_br  = c1.number_input("Gols Brasil", min_value=0, max_value=20,
                                    value=int(dados_usuario["placar_brasil"][b]),
                                    step=1, key=f"gbr_{idx}")
            g_adv = c2.number_input("Gols Adversário", min_value=0, max_value=20,
                                    value=int(dados_usuario["placar_brasil"][b + 1]),
                                    step=1, key=f"gadv_{idx}")
            palpites_gols[b] = g_br; palpites_gols[b + 1] = g_adv

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Trava ─────────────────────────────────────────────────────────────────
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
            </div>""", unsafe_allow_html=True)
            col_sim, col_nao = st.columns(2)
            if col_sim.button("🔥 Sim, quero travar!", key="btn_sim"):
                banco_atual = carregar_banco()
                if banco_atual[usuario_selecionado]["travado"]:
                    st.warning("Seus palpites já estavam travados. Nenhuma alteração feita.")
                else:
                    banco_atual[usuario_selecionado]["classificacao"] = {
                        g: list(palpites_grupos.get(g, v)) for g, v in GRUPOS_CONFIG.items()
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
        st.info("🔒 Disponível após o encerramento da fase de grupos e definição oficial do chaveamento da Copa 2026.")
        st.markdown("### Prévia dos confrontos")
    col_mm1, col_mm2 = st.columns(2)
    for i, conf in enumerate(MATA_MATA_CONFRONTOS):
        col = col_mm1 if i % 2 == 0 else col_mm2
        with col:
            st.markdown(f'<div class="mm-card"><div class="mm-id">Confronto {conf["id"]}</div>'
                        f'<div class="mm-times">{conf["t1"]} vs {conf["t2"]}</div></div>',
                        unsafe_allow_html=True)
            venc = dados_usuario["vencedores_mata_mata"].get(conf["id"], "")
            opts = ["— escolher —", conf["t1"], conf["t2"]]
            idx_a = opts.index(venc) if venc in opts else 0
            st.radio("Quem avança?", options=opts, index=idx_a,
                     key=f"mm_{conf['id']}",
                     disabled=(not MATA_MATA_LIBERADO) or dados_usuario["travado"] or modo_view_only,
                     label_visibility="collapsed")

# ──────────────────────────────────────────────────────────────────────────────
# ABA 3: CALENDÁRIO
# ──────────────────────────────────────────────────────────────────────────────
with aba_calendario:
    st.markdown("## 📅 Calendário da Copa 2026")

    # Indicador de fonte da API
    fonte = api_data["fonte"]
    cls_fonte = "api-status-ok" if "✓" in fonte else "api-status-err"
    st.markdown(
        f'<div style="text-align:right;margin-bottom:6px;">'
        f'Fonte: <span class="{cls_fonte}">{fonte}</span> &nbsp;'
        f'<span style="font-size:11px;color:#94a3b8;">Horários em BRT (Brasília)</span></div>',
        unsafe_allow_html=True
    )

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
            status       = _status_jogo(j["data"], j["hora_brt"])
            brasil_class = "jogo-brasil" if j["brasil"] else ""
            hora_d       = _hora_display(j["hora_brt"])

            if status == "finalizado":
                badge = '<span class="badge-finalizado">✓ Finalizado</span>'
            elif status == "aovivo":
                badge = '<span class="badge-aovivo">🔴 Ao vivo</span>'
            else:
                badge = '<span class="badge-previsto">Previsto</span>'

            st.markdown(f"""
            <div class="jogo-card {brasil_class}">
                <div class="jogo-data">{j["data"]}</div>
                <div class="jogo-hora">{hora_d}</div>
                <div>
                    <div class="jogo-nome">{j["jogo"]}</div>
                    <div class="jogo-local">📍 {j["local"]}</div>
                </div>
                {badge}
            </div>""", unsafe_allow_html=True)

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
        </div>""", unsafe_allow_html=True)

    linhas = []
    qualquer_jogo_realizado = (
        any(g is not None for g in api_data["gols_brasil"]) or
        len(_grupos_com_resultado()) > 0
    )

    for amigo in AMIGOS:
        user          = st.session_state.banco[amigo]
        total, det    = _calcular_pontuacao(amigo)
        travado       = user["travado"]
        badges        = []

        if travado:
            acertou_placar = any(
                user["placar_brasil"][i*2]   == api_data["gols_brasil"][i*2] and
                user["placar_brasil"][i*2+1] == api_data["gols_brasil"][i*2+1] and
                api_data["gols_brasil"][i*2] is not None
                for i in range(3)
            )
            errou_tudo = qualquer_jogo_realizado and total == 0
            if acertou_placar:
                badges.append("🔮 Profeta")
            if errou_tudo:
                badges.append("🤡 Zica")

        linhas.append({"amigo": amigo, "total": total, "travado": travado,
                       "badges": badges, "detalhes": det})

    linhas.sort(key=lambda x: (-int(x["travado"]), -x["total"]))

    travados_pts = [l for l in linhas if l["travado"] and l["total"] > 0]
    if len(travados_pts) > 0:
        linhas[0]["badges"].insert(0, "👑 Líder")
        if len(travados_pts) > 1:
            linhas[-1]["badges"].append("🔦 Lanterna")

    posicao_icons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣"]

    for i, linha in enumerate(linhas):
        cor_borda = "border: 2px solid #1d4ed8;" if i == 0 and linha["total"] > 0 else ""
        badge_str = " | ".join(linha["badges"]) if linha["badges"] else \
                    ("⏳ Aguardando início" if not qualquer_jogo_realizado else "🏃 Em jogo")
        pts_color = "#1e3a5f" if linha["total"] > 0 else "#94a3b8"

        st.markdown(f"""
        <div class="rank-row" style="{cor_borda}">
            <div class="rank-pos">{posicao_icons[i]}</div>
            <div style="flex:1">
                <div class="rank-nome">{linha["amigo"]}</div>
                <div class="rank-badges">{badge_str}</div>
                <div class="{'rank-status-lock' if linha['travado'] else 'rank-status-open'}">
                    {'🔒 Travado' if linha['travado'] else '🔓 Editando'}
                </div>
            </div>
            <div>
                <div class="rank-pts" style="color:{pts_color}">{linha["total"]}</div>
                <div class="rank-pts-label">pts</div>
            </div>
        </div>""", unsafe_allow_html=True)

    if not qualquer_jogo_realizado:
        st.info("⏳ A pontuação começa a ser calculada após o primeiro jogo da Copa.")

    st.markdown("---")
    st.markdown("### Detalhamento por amigo")
    for linha in linhas:
        if linha["travado"] and linha["detalhes"]:
            with st.expander(f"{linha['amigo']} — {linha['total']} pts"):
                for cat, pts in linha["detalhes"]:
                    st.markdown(f"- **{cat}**: {pts} pts")
        elif not linha["travado"]:
            with st.expander(f"{linha['amigo']} — palpite em aberto"):
                st.caption("Ainda não travou os palpites.")
