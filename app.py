import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime, timezone

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

# Próximo jogo do Brasil para o countdown
PROXIMO_JOGO_BRASIL = {
    "nome":  "Brasil x Marrocos",
    "data_hora": datetime(2026, 6, 13, 22, 0, 0, tzinfo=timezone.utc),  # 19h Brasília = 22h UTC
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

        # HTTP 401 = chave errada; 404 = bin_id errado
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
    Retorna True se bem-sucedido, False caso contrário.
    """
    try:
        bin_id  = st.secrets.get("JSONBIN_ID", "")
        api_key = st.secrets.get("JSONBIN_KEY", "")
        if not bin_id or not api_key:
            # Modo offline: só salva na sessão
            st.session_state.banco = banco_completo
            return True

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
    "Cape Verde": "Cabo Verde", "Saudi Arabia": "Arábia Saudita", "Spain": "Espanha", "Uruguay": "Uruguai",
    "France": "França", "Iraq": "Iraque", "Norway": "Noruega", "Senegal": "Senegal",
    "Algeria": "Argélia", "Argentina": "Argentina", "Austria": "Áustria", "Jordan": "Jordânia",
    "Colombia": "Colômbia", "DR Congo": "RD Congo", "Portugal": "Portugal", "Uzbekistan": "Uzbequistão",
    "Croatia": "Croácia", "England": "Inglaterra", "Ghana": "Gana", "Panama": "Panamá",
}

def _montar_resultado(jogos_reais, fonte):
    """Constrói o dict de retorno padrão a partir de uma lista de jogos processados."""
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
        "fonte":             fonte,
        "classificacao_real": {g: list(t) for g, t in GRUPOS_CONFIG.items()},
        "jogos_reais":       jogos_reais,
        "gols_brasil":       gols_brasil,
    }

@st.cache_data(ttl=600)
def obter_resultados():
    """
    Tenta as 3 APIs em sequência. Se todas falharem, usa calendário fixo.
    Ordem: 1) football-data.org  2) Zafronix  3) Sportmonks
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
            url = "https://api.football-data.org/v4/competitions/WC/matches?season=2026"
            r = requests.get(url, headers={"X-Auth-Token": token}, timeout=6)
            if r.status_code == 200:
                matches = r.json().get("matches", [])
                if matches:
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
                    return _montar_resultado(jogos, "football-data.org")
    except Exception:
        pass

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
                    t_c = TRADUCAO.get(m.get("home_team", ""), m.get("home_team", ""))
                    t_f = TRADUCAO.get(m.get("away_team", ""), m.get("away_team", ""))
                    gc  = m.get("home_score")
                    gf  = m.get("away_score")
                    st_ = m.get("status", "SCHEDULED")
                    jogos.append({
                        "jogo":     f"{t_c} x {t_f}",
                        "placar_c": gc,
                        "placar_f": gf,
                        "status":   "FINISHED" if st_ == "FINISHED" else st_,
                    })
                return _montar_resultado(jogos, "Zafronix Sports API")
    except Exception:
        pass

    # ── API 3: Sportmonks Football API ────────────────────────────────────────
    try:
        token_sm = st.secrets.get("SPORTMONKS_TOKEN", "Sdy1n1ctP5Q0ovO9NkVPZ5ey8Pfxqg2dRYRCmJl8lqjuk2MWw9ADP9ctWOUm")
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
                    t_c = TRADUCAO.get(participants[0].get("name", ""), participants[0].get("name", ""))
                    t_f = TRADUCAO.get(participants[1].get("name", ""), participants[1].get("name", ""))
                    scores = m.get("scores", {})
                    gc  = scores.get("localteam_score")
                    gf  = scores.get("visitorteam_score")
                    st_ = m.get("state", {})
                    state_name = st_.get("name", "") if isinstance(st_, dict) else str(st_)
                    ended = state_name in ("FT", "ENDED", "AET", "PEN")
                    jogos.append({
                        "jogo":     f"{t_c} x {t_f}",
                        "placar_c": gc,
                        "placar_f": gf,
                        "status":   "FINISHED" if ended else "SCHEDULED",
                    })
                if jogos:
                    return _montar_resultado(jogos, "Sportmonks")
    except Exception:
        pass

    # ── Fallback: calendário fixo ─────────────────────────────────────────────
    return padrao

api_data = obter_resultados()

# ==============================================================================
# HELPERS
# ==============================================================================
def _status_jogo(data_str: str, hora_str: str):
    """Retorna 'finalizado', 'aovivo' ou 'previsto' baseado na data/hora atual."""
    try:
        h_num = hora_str.replace("h", ":").rstrip(":")
        if len(h_num) <= 5:
            dt = datetime.strptime(f"2026/{data_str} {h_num}", "%Y/%d/%m %H:%M")
        else:
            return "previsto"
        now   = datetime.now()
        delta = (now - dt).total_seconds() / 60
        if delta > 110:
            return "finalizado"
        if 0 <= delta <= 110:
            return "aovivo"
        return "previsto"
    except Exception:
        return "previsto"

def _countdown_brasil():
    """Retorna string do countdown para o próximo jogo do Brasil."""
    agora = datetime.now(timezone.utc)
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
    Enquanto nenhum jogo ocorreu (ou a API só retornou o calendário fixo),
    o set fica vazio e nenhum grupo pontua.
    """
    finalizados = set()
    jogos_reais = api_data.get("jogos_reais", [])
    if not jogos_reais:
        return finalizados  # API não retornou nada real ainda

    for nome_grupo, times in GRUPOS_CONFIG.items():
        for jogo in jogos_reais:
            if jogo.get("status") != "FINISHED":
                continue
            # Verifica se algum dos times do grupo aparece no jogo
            partes = jogo["jogo"].replace(" x ", "|").split("|")
            t_c = partes[0].strip() if len(partes) > 0 else ""
            t_f = partes[1].strip() if len(partes) > 1 else ""
            if t_c in times or t_f in times:
                finalizados.add(nome_grupo)
                break  # basta um jogo finalizado neste grupo

    return finalizados


def _calcular_pontuacao(amigo):
    """Calcula pontuação de um amigo. Retorna (total, detalhes)."""
    user     = st.session_state.banco[amigo]
    real     = api_data
    total    = 0
    detalhes = []

    if not user["travado"]:
        return 0, []

    # Grupos com ao menos 1 jogo finalizado — único momento em que pontua
    grupos_ativos = _grupos_com_resultado()

    pts_grupos = 0
    for g in GRUPOS_CONFIG:
        if g not in grupos_ativos:
            continue  # Nenhum jogo deste grupo terminou ainda — não pontua
        if user["classificacao"][g][0] == real["classificacao_real"][g][0]:
            pts_grupos += 2
        if user["classificacao"][g][1] == real["classificacao_real"][g][1]:
            pts_grupos += 2
    total += pts_grupos
    detalhes.append(("Fase de grupos", pts_grupos))

    # Jogos do Brasil — 5 pts placar exato, 3 pts vencedor/empate correto
    pts_brasil = 0
    for i in range(3):
        b     = i * 2
        p_br  = user["placar_brasil"][b]
        p_adv = user["placar_brasil"][b + 1]
        r_br  = real["gols_brasil"][b]
        r_adv = real["gols_brasil"][b + 1]
        if r_br is None or r_adv is None:
            continue  # Jogo ainda não ocorreu — não pontua
        if p_br == r_br and p_adv == r_adv:
            pts_brasil += 5
        elif (
            (p_br > p_adv and r_br > r_adv) or
            (p_br < p_adv and r_br < r_adv) or
            (p_br == p_adv and r_br == r_adv)
        ):
            pts_brasil += 3
    total += pts_brasil
    detalhes.append(("Jogos do Brasil", pts_brasil))
    return total, detalhes

# ==============================================================================
# CABEÇALHO
# ==============================================================================
st.markdown("# 🏆 Bolão do Bobão — Copa 2026")

# Countdown
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

# Sempre re-lê o estado REAL deste usuário do banco (garante que trava seja respeitada)
dados_usuario = st.session_state.banco[usuario_selecionado]

# Verifica se já está autenticado
autenticado    = (st.session_state.usuario_autenticado == usuario_selecionado)
modo_view_only = False   # será True se olhar palpites de outro

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
                # PIN correto — sincroniza com o banco remoto
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

# Se não autenticado, entra em modo somente-leitura
if not autenticado:
    modo_view_only = True

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
    if modo_view_only:
        st.markdown(
            f'<div class="view-banner">👁 Modo visualização — faça login com seu PIN para editar</div>',
            unsafe_allow_html=True
        )
    elif dados_usuario["travado"]:
        st.markdown(
            '<div class="status-travado">🔒 Palpites travados! Boa sorte, cuzão! 🍀</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-editando">✏️ Editando — defina a classificação de cada grupo e trave antes do 1º jogo!</div>',
            unsafe_allow_html=True
        )

    travado_ou_view = dados_usuario["travado"] or modo_view_only
    palpites_grupos = {}

    st.markdown("## 📊 Classificação dos Grupos")

    for nome_grupo, lista_times in GRUPOS_CONFIG.items():
        st.markdown(f'<div class="group-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="group-header">{nome_grupo}</div>', unsafe_allow_html=True)

        ordem = list(dados_usuario["classificacao"].get(nome_grupo, lista_times))
        # Garante que todos os times do grupo estejam na ordem (migração de dados antigos)
        for t in lista_times:
            if t not in ordem:
                ordem.append(t)
        ordem = [t for t in ordem if t in lista_times]

        if travado_ou_view:
            st.markdown(
                f"🥇 **{ordem[0]}** &nbsp;|&nbsp; 🥈 **{ordem[1]}** &nbsp;|&nbsp; "
                f"🥉 {ordem[2]} &nbsp;|&nbsp; ❌ {ordem[3]}",
                unsafe_allow_html=True
            )
            palpites_grupos[nome_grupo] = ordem
        else:
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

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Jogos do Brasil ──
    st.markdown("## 🇧🇷 Jogos do Brasil — Grupo C")

    palpites_gols = list(dados_usuario["placar_brasil"])

    for idx, jogo_info in enumerate(JOGOS_BRASIL):
        st.markdown(f'<div class="group-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="group-header-br">🗓 {jogo_info["jogo"]} — {jogo_info["data"]} {jogo_info["hora"]}</div>',
                    unsafe_allow_html=True)
        st.caption(f"📍 {jogo_info['loc']}")

        b = idx * 2
        c1, c2 = st.columns(2)
        g_br  = c1.number_input("Gols Brasil", min_value=0, max_value=20,
                                value=int(dados_usuario["placar_brasil"][b]),
                                step=1, key=f"gbr_{idx}",
                                disabled=travado_ou_view)
        g_adv = c2.number_input("Gols Adversário", min_value=0, max_value=20,
                                value=int(dados_usuario["placar_brasil"][b + 1]),
                                step=1, key=f"gadv_{idx}",
                                disabled=travado_ou_view)
        palpites_gols[b]     = g_br
        palpites_gols[b + 1] = g_adv
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Trava ──
    if not travado_ou_view:
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
                    banco_atual[usuario_selecionado]["classificacao"]  = {g: list(palpites_grupos.get(g, v))
                                                                           for g, v in GRUPOS_CONFIG.items()}
                    banco_atual[usuario_selecionado]["placar_brasil"]  = palpites_gols
                    banco_atual[usuario_selecionado]["travado"]        = True
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
                disabled=(not MATA_MATA_LIBERADO) or travado_ou_view,
                label_visibility="collapsed"
            )

# ──────────────────────────────────────────────────────────────────────────────
# ABA 3: CALENDÁRIO
# ──────────────────────────────────────────────────────────────────────────────
with aba_calendario:
    st.markdown("## 📅 Calendário da Copa 2026")

    st.markdown(f'<div class="fonte-dados">Fonte: {api_data["fonte"]}</div>', unsafe_allow_html=True)

    # Filtros
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        filtro_brasil = st.toggle("🇧🇷 Só jogos do Brasil", value=False, key="filtro_br")
    with col_f2:
        grupos_disponiveis = sorted({
            j["jogo"].split(" x ")[0].strip() for j in CALENDARIO_FIXO
        })
        filtro_sel = st.selectbox("Filtrar por seleção:", ["Todas"] + sorted({
            t for j in CALENDARIO_FIXO for t in j["jogo"].replace(" x ", "|").split("|")
        }), key="filtro_sel")

    jogos_exibir = CALENDARIO_FIXO
    if filtro_brasil:
        jogos_exibir = [j for j in jogos_exibir if j["brasil"]]
    if filtro_sel != "Todas":
        jogos_exibir = [j for j in jogos_exibir if filtro_sel in j["jogo"]]

    # Agrupar por data
    datas = []
    for j in jogos_exibir:
        if j["data"] not in datas:
            datas.append(j["data"])

    for data in datas:
        st.markdown(f'<div class="data-header">📆 {data}</div>', unsafe_allow_html=True)
        jogos_data = [j for j in jogos_exibir if j["data"] == data]
        for j in jogos_data:
            status = _status_jogo(j["data"], j["hora"])
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
                    <div class="jogo-nome">{j["jogo"]}</div>
                    <div class="jogo-local">📍 {j["local"]}</div>
                </div>
                {badge}
            </div>
            """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# ABA 4: RANKING
# ──────────────────────────────────────────────────────────────────────────────
with aba_ranking:
    st.markdown("## 🥇 Ranking Geral")

    # Regras de pontuação
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

    # Monta tabela
    linhas = []
    qualquer_jogo_realizado = any(g is not None for g in api_data["gols_brasil"])

    for amigo in AMIGOS:
        user   = st.session_state.banco[amigo]
        total, detalhes = _calcular_pontuacao(amigo)
        travado = user["travado"]

        badges = []
        if travado:
            # Verifica acerto de placar exato
            acertou_placar = any(
                user["placar_brasil"][i * 2]     == api_data["gols_brasil"][i * 2] and
                user["placar_brasil"][i * 2 + 1] == api_data["gols_brasil"][i * 2 + 1] and
                api_data["gols_brasil"][i * 2] is not None
                for i in range(3)
            )
            # Verifica se errou tudo (apenas se algum jogo já ocorreu)
            errou_tudo = qualquer_jogo_realizado and total == 0

            if acertou_placar:
                badges.append("🔮 Profeta")
            if errou_tudo:
                badges.append("🤡 Zica")

        linhas.append({
            "amigo":   amigo,
            "total":   total,
            "travado": travado,
            "badges":  badges,
            "detalhes": detalhes,
        })

    # Ordena: travados primeiro, depois por pontuação
    linhas.sort(key=lambda x: (-int(x["travado"]), -x["total"]))

    # Adiciona badges de posição
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

    # Detalhamento por amigo (expander)
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
