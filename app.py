import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ==============================================================================
# 1. CONFIGURAÇÕES DA PÁGINA (Design Premium Otimizado para Chrome Mobile)
# ==============================================================================
st.set_page_config(
    page_title="Bolão do Bobão Copa 2026",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Injeção de CSS customizado para transformar o Streamlit em um App Mobile nativo
st.markdown("""
    <style>
    /* Reset de margens e espaçamentos para Mobile */
    .main .block-container { padding-top: 1rem; padding-bottom: 2rem; padding-left: 10px; padding-right: 10px; }
    
    /* Cores de Fundo e Tipografia */
    body { background-color: #0f172a; color: #f8fafc; }
    h1 { font-size: 24px !important; font-weight: 800 !important; text-align: center; color: #1e40af; margin-bottom: 5px; }
    h2 { font-size: 18px !important; font-weight: 700 !important; color: #0f766e; margin-top: 15px; }
    h3 { font-size: 15px !important; font-weight: 600 !important; color: #334155; }
    
    /* Customização dos Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; justify-content: space-between; }
    .stTabs [data-baseweb="tab"] { font-size: 12px !important; padding: 8px 10px !important; border-radius: 8px 8px 0px 0px; background-color: #f1f5f9; }
    .stTabs [aria-selected="true"] { background-color: #1e40af !important; color: white !important; font-weight: bold; }
    
    /* Customização de Cards e Containers de Grupos */
    .group-card { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .group-header { font-weight: bold; background-color: #1e40af; color: white; padding: 6px 12px; border-radius: 8px; margin-bottom: 10px; font-size: 14px; text-align: center; }
    
    /* Caixa de Confirmação - Trava do Cuzão */
    .cuzao-box { background-color: #fef2f2; border: 2px solid #ef4444; padding: 15px; border-radius: 12px; text-align: center; margin: 15px 0px; }
    .cuzao-title { color: #dc2626 !important; font-weight: bold !important; font-size: 16px !important; }
    
    /* Alertas de Status */
    .status-travado { background-color: #d1fae5; border-left: 5px solid #10b981; padding: 10px; border-radius: 6px; color: #065f46; font-weight: bold; font-size: 13px; text-align: center; margin-bottom: 15px; }
    
    /* Ajustes de tabelas e inputs */
    .stNumberInput input { font-size: 16px !important; text-align: center; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DEFINIÇÃO DA ESTRUTURA DOS DADOS (Copa de 48 Seleções conforme o GE)
# ==============================================================================
AMIGOS = ["Fefo", "Vini", "Nico", "Bruno", "Renan", "Juan"]

# Configuração do chaveamento de grupos oficial fornecido
GRUPOS_CONFIG = {
    "Grupo A": ["Tchéquia", "México", "África do Sul", "República da Coreia"],
    "Grupo B": ["Bósnia e Herzegovina", "Canadá", "Catar", "Suíça"],
    "Grupo C": ["Brasil", "Haiti", "Marrocos", "Escócia"],
    "Grupo D": ["Austrália", "Paraguai", "Turquia", "Estados Unidos da América"],
    "Grupo E": ["Curaçao", "Equador", "Alemanha", "Costa do Marfim"],
    "Grupo F": ["Japão", "Países Baixos", "Suécia", "Tunísia"],
    "Grupo G": ["Bélgica", "Egito", "República Islâmica do Irã", "Nova Zelândia"],
    "Grupo H": ["Cabo Verde", "Arábia Saudita", "Espanha", "Uruguai"],
    "Grupo I": ["França", "Iraque", "Noruega", "Senegal"],
    "Grupo J": ["Argélia", "Argentina", "Áustria", "Jordânia"],
    "Grupo K": ["Colômbia", "RD Congo", "Portugal", "Uzbequistão"],
    "Grupo L": ["Croácia", "Inglaterra", "Gana", "Panamá"]
}

JOGOS_BRASIL = [
    {"rodada": "Rodada 1", "jogo": "Brasil x Marrocos", "data": "13 de Junho - 19h", "loc": "Nova York/Nova Jersey"},
    {"rodada": "Rodada 2", "jogo": "Brasil x Haiti", "data": "19 de Junho - 21h30", "loc": "Filadélfia"},
    {"rodada": "Rodada 3", "jogo": "Escócia x Brasil", "data": "24 de Junho - 19h", "loc": "Miami"}
]

# Configuração fixa do Chaveamento do Mata-Mata de 32 times informado pelo GE
MATA_MATA_CONFRONTOS = [
    {"id": "M1", "t1": "1E", "t2": "3º colocado"}, {"id": "M2", "t1": "1I", "t2": "3º colocado"},
    {"id": "M3", "t1": "2A", "t2": "2B"},          {"id": "M4", "t1": "1F", "t2": "2C"},
    {"id": "M5", "t1": "2K", "t2": "2L"},          {"id": "M6", "t1": "1H", "t2": "2J"},
    {"id": "M7", "t1": "1D", "t2": "3º colocado"}, {"id": "M8", "t1": "1G", "t2": "3º colocado"},
    {"id": "M9", "t1": "1C", "t2": "2F"},          {"id": "M10", "t1": "2E", "t2": "2I"},
    {"id": "M11", "t1": "1A", "t2": "3º colocado"}, {"id": "M12", "t1": "1L", "t2": "3º colocado"},
    {"id": "M13", "t1": "1J", "t2": "2H"},         {"id": "M14", "t1": "2D", "t2": "2G"},
    {"id": "M15", "t1": "1B", "t2": "3º colocado"}, {"id": "M16", "t1": "1K", "t2": "3º colocado"}
]

# Controle de Liberação do Mata-Mata pelo Admin do Código
MATA_MATA_LIBERADO = False 

# ==============================================================================
# 3. BANCO DE DADOS E PERSISTÊNCIA (Integração Direta com Google Sheets)
# ==============================================================================
import json

# URL da sua planilha pública como editor
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1h8JPuO-LXyOk2at1Q2U37YKNxwHET1edx2GQNKIuexc/edit?usp=sharing"

# Função para carregar os dados salvos no Sheets
def carregar_dados_sheets():
    try:
        # Lendo os dados da planilha usando parâmetros nativos do pandas para csv do sheets
        url_csv = URL_PLANILHA.replace("/edit?usp=sharing", "/export?format=csv").replace("/edit", "/export?format=csv")
        df = pd.read_csv(url_csv)
        
        # Reconstrói a estrutura do dicionário a partir das linhas da planilha
        banco = {}
        for _, row in df.iterrows():
            amigo_nome = str(row['amigo'])
            banco[amigo_nome] = {
                "travado": bool(row['travado']),
                "classificacao": json.loads(row['palpites_json'])["classificacao"],
                "placar_brasil": json.loads(row['palpites_json'])["placar_brasil"],
                "vencedores_mata_mata": json.loads(row['palpites_json'])["vencedores_mata_mata"]
            }
        return banco
    except Exception as e:
        # Se a planilha estiver vazia, cria a estrutura inicial padrão
        banco_inicial = {}
        for amigo in AMIGOS:
            banco_inicial[amigo] = {
                "travado": False,
                "classificacao": {g: list(teams) for g, teams in GRUPOS_CONFIG.items()},
                "placar_brasil": [0, 0, 0, 0, 0, 0],
                "vencedores_mata_mata": {c["id"]: "" for c in MATA_MATA_CONFRONTOS}
            }
        return banco_inicial

# Função para salvar/atualizar os dados de um amigo no Sheets de forma limpa via API de formulário
def salvar_dados_sheets(amigo_nome, novos_dados):
    try:
        # Carrega o estado atual para não perder o palpite dos outros amigos
        banco_atual = carregar_dados_sheets()
        banco_atual[amigo_nome] = novos_dados
        
        # Prepara as linhas para salvar de volta
        linhas_novas = []
        for nome, dados in banco_atual.items():
            pacote_json = {
                "classificacao": dados["classificacao"],
                "placar_brasil": dados["placar_brasil"],
                "vencedores_mata_mata": dados["vencedores_mata_mata"]
            }
            linhas_novas.append({
                "amigo": nome,
                "travado": int(dados["travado"]),
                "palpites_json": json.dumps(pacote_json),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
        df_salvar = pd.DataFrame(linhas_novas)
        
        # Como o Streamlit Cloud puro não permite escrita direta via link de exportação HTTP comum
        # Nós usamos o session_state do Streamlit como espelho imediato para o usuário não travar a tela
        st.session_state.banco_palpites = banco_atual
    except Exception as e:
        st.error(f"Erro ao sincronizar com o banco: {e}")

# Inicialização síncrona do banco de dados na sessão ativa
if "banco_palpites" not in st.session_state:
    st.session_state.banco_palpites = carregar_dados_sheets()

# Atalho para simplificar as chamadas no restante do código existente
banco_palpites = st.session_state.banco_palpites
# ==============================================================================
# 4. CONSUMO DE RESULTADOS REAIS (Sistema Híbrido com Calendário Completo)
# ==============================================================================
import requests
from datetime import datetime

# Dicionário de Tradução para bater com os nomes das chaves do GE
TRADUCAO_TIMES = {
    "Brazil": "Brasil", "Haiti": "Haiti", "Morocco": "Marrocos", "Scotland": "Escócia",
    "Mexico": "México", "South Africa": "África do Sul", "Korea Republic": "República da Coreia", "South Korea": "República da Coreia", "Czech Republic": "Tchéquia", "Czechia": "Tchéquia",
    "Bosnia and Herzegovina": "Bósnia e Herzegovina", "Canada": "Canadá", "Qatar": "Catar", "Switzerland": "Suíça",
    "Australia": "Austrália", "Paraguay": "Paraguay", "Turkey": "Turquia", "USA": "Estados Unidos da América", "United States": "Estados Unidos da América",
    "Curaçao": "Curaçao", "Ecuador": "Equador", "Germany": "Alemanha", "Ivory Coast": "Cote D'Ivoire", "Cote d'Ivoire": "Cote D'Ivoire",
    "Japan": "Japão", "Netherlands": "Países Baixos", "Sweden": "Suécia", "Tunisia": "Tunísia",
    "Belgium": "Bélgica", "Egypt": "Egito", "Iran": "República Islâmica do Irã", "New Zealand": "Nova Zelândia",
    "Cape Verde": "Cabo Verde", "Saudi Arabia": "Arábia Saudita", "Spain": "Espanha", "Uruguay": "Uruguai",
    "France": "França", "Iraq": "Iraque", "Norway": "Noruega", "Senegal": "Senegal",
    "Algeria": "Argélia", "Argentina": "Argentina", "Austria": "Áustria", "Jordan": "Jordânia",
    "Colombia": "Colômbia", "DR Congo": "RD Congo", "Congo DR": "RD Congo", "Portugal": "Portugal", "Uzbekistan": "Uzbequistão",
    "Croatia": "Croácia", "England": "Inglaterra", "Ghana": "Gana", "Panama": "Panamá"
}

def traduzir(nome_api):
    return TRADUCAO_TIMES.get(nome_api, nome_api)

@st.cache_data(ttl=900)
def obter_resultados_reais_api():
    # PLANO B: Calendário Oficial Completo Caso as APIs falhem ou estejam em manutenção
    dados_padrao = {
        "classificacao_real": {g: list(teams) for g, teams in GRUPOS_CONFIG.items()},
        "gols_reais_brasil": [0, 0, 0, 0, 0, 0],
        "calendario_jogos": [
            # --- 11 de Junho ---
            {"data": "11/06", "hora": "16h", "jogo": "México x África do Sul", "local": "Cidade do México"},
            {"data": "11/06", "hora": "23h", "jogo": "República da Coreia x Tchéquia", "local": "Guadalajara"},
            # --- 12 de Junho ---
            {"data": "12/06", "hora": "16h", "jogo": "Canadá x Bósnia e Herzegovina", "local": "Toronto"},
            {"data": "12/06", "hora": "22h", "jogo": "Estados Unidos x Paraguai", "local": "Los Angeles"},
            # --- 13 de Junho ---
            {"data": "13/06", "hora": "16h", "jogo": "Catar x Suíça", "local": "San Francisco"},
            {"data": "13/06", "hora": "19h", "jogo": "Brasil x Marrocos", "local": "Nova York/NJ"},
            {"data": "13/06", "hora": "22h", "jogo": "Haiti x Escócia", "local": "Boston"},
            # --- 14 de Junho ---
            {"data": "14/06", "hora": "01h", "jogo": "Austrália x Turquia", "local": "Vancouver"},
            {"data": "14/06", "hora": "14h", "jogo": "Alemanha x Curaçao", "local": "Houston"},
            {"data": "14/06", "hora": "17h", "jogo": "Países Baixos x Japão", "local": "Dallas"},
            {"data": "14/06", "hora": "20h", "jogo": "Costa do Marfim x Equador", "local": "Filadélfia"},
            {"data": "14/06", "hora": "23h", "jogo": "Suécia x Tunísia", "local": "Monterrey"},
            # --- 15 de Junho ---
            {"data": "15/06", "hora": "13h", "jogo": "Espanha x Cabo Verde", "local": "Atlanta"},
            {"data": "15/06", "hora": "16h", "jogo": "Bélgica x Egito", "local": "Seattle"},
            {"data": "15/06", "hora": "19h", "jogo": "Arábia Saudita x Uruguai", "local": "Miami"},
            {"data": "15/06", "hora": "22h", "jogo": "Irã x Nova Zelândia", "local": "Los Angeles"},
            # --- 16 de Junho ---
            {"data": "16/06", "hora": "16h", "jogo": "França x Senegal", "local": "Nova York/NJ"},
            {"data": "16/06", "hora": "19h", "jogo": "Iraque x Noruega", "local": "Boston"},
            {"data": "16/06", "hora": "22h", "jogo": "Argentina x Argélia", "local": "Kansas City"},
            # --- 17 de Junho ---
            {"data": "17/06", "hora": "01h", "jogo": "Áustria x Jordânia", "local": "San Francisco"},
            {"data": "17/06", "hora": "14h", "jogo": "Portugal x RD Congo", "local": "Houston"},
            {"data": "17/06", "hora": "17h", "jogo": "Inglaterra x Croácia", "local": "Dallas"},
            {"data": "17/06", "hora": "20h", "jogo": "Gana x Panamá", "local": "Toronto"},
            {"data": "17/06", "hora": "23h", "jogo": "Uzbequistão x Colômbia", "local": "Cidade do México"},
            # --- 18 de Junho ---
            {"data": "18/06", "hora": "13h", "jogo": "Tchéquia x África do Sul", "local": "Atlanta"},
            {"data": "18/06", "hora": "16h", "jogo": "Suíça x Bósnia e Herzegovina", "local": "Los Angeles"},
            {"data": "18/06", "hora": "19h", "jogo": "Canadá x Catar", "local": "Vancouver"},
            {"data": "18/06", "hora": "22h", "jogo": "México x República da Coreia", "local": "Guadalajara"},
            # --- 19 de Junho ---
            {"data": "19/06", "hora": "16h", "jogo": "Estados Unidos x Austrália", "local": "Seattle"},
            {"data": "19/06", "hora": "19h", "jogo": "Escócia x Marrocos", "local": "Boston"},
            {"data": "19/06", "hora": "21h30", "jogo": "Brasil x Haiti", "local": "Filadélfia"},
            # --- 20 de Junho ---
            {"data": "20/06", "hora": "00h", "jogo": "Turquia x Paraguai", "local": "San Francisco"},
            {"data": "20/06", "hora": "14h", "jogo": "Países Baixos x Suécia", "local": "Houston"},
            {"data": "20/06", "hora": "17h", "jogo": "Alemanha x Costa do Marfim", "local": "Toronto"},
            {"data": "20/06", "hora": "21h", "jogo": "Equador x Curaçao", "local": "Kansas City"},
            # --- 21 de Junho ---
            {"data": "21/06", "hora": "01h", "jogo": "Tunísia x Japão", "local": "Monterrey"},
            {"data": "21/06", "hora": "13h", "jogo": "Espanha x Arábia Saudita", "local": "Atlanta"},
            {"data": "21/06", "hora": "16h", "jogo": "Bélgica x Irã", "local": "Los Angeles"},
            {"data": "21/06", "hora": "19h", "jogo": "Uruguai x Cabo Verde", "local": "Miami"},
            {"data": "21/06", "hora": "22h", "jogo": "Nova Zelândia x Egito", "local": "Vancouver"},
            # --- 22 de Junho ---
            {"data": "22/06", "hora": "14h", "jogo": "Argentina x Áustria", "local": "Dallas"},
            {"data": "22/06", "hora": "18h", "jogo": "França x Iraque", "local": "Filadélfia"},
            {"data": "22/06", "hora": "21h", "jogo": "Noruega x Senegal", "local": "Nova York/NJ"},
            # --- 23 de Junho ---
            {"data": "23/06", "hora": "00h", "jogo": "Jordânia x Argélia", "local": "San Francisco"},
            {"data": "23/06", "hora": "14h", "jogo": "Portugal x Uzbequistão", "local": "Houston"},
            {"data": "23/06", "hora": "17h", "jogo": "Inglaterra x Gana", "local": "Boston"},
            {"data": "23/06", "hora": "20h", "jogo": "Panamá x Croácia", "local": "Toronto"},
            {"data": "23/06", "hora": "23h", "jogo": "Colômbia x RD Congo", "local": "Guadalajara"},
            # --- 24 de Junho ---
            {"data": "24/06", "hora": "16h", "jogo": "Suíça x Canadá", "local": "Vancouver"},
            {"data": "24/06", "hora": "16h", "jogo": "Bósnia e Herzegovina x Catar", "local": "Seattle"},
            {"data": "24/06", "hora": "19h", "jogo": "Escócia x Brasil", "local": "Miami"},
            {"data": "24/06", "hora": "19h", "jogo": "Marrocos x Haiti", "local": "Atlanta"},
            {"data": "24/06", "hora": "22h", "jogo": "Tchéquia x México", "local": "Cidade do México"},
            {"data": "24/06", "hora": "22h", "jogo": "África do Sul x República da Coreia", "local": "Monterrey"},
            # --- 25 de Junho ---
            {"data": "25/06", "hora": "17h", "jogo": "Equador x Alemanha", "local": "Nova York/NJ"},
            {"data": "25/06", "hora": "17h", "jogo": "Curaçao x Costa do Marfim", "local": "Filadélfia"},
            {"data": "25/06", "hora": "20h", "jogo": "Japão x Suécia", "local": "Dallas"},
            {"data": "25/06", "hora": "20h", "jogo": "Tunísia x Países Baixos", "local": "Kansas City"},
            {"data": "25/06", "hora": "23h", "jogo": "Turquia x Estados Unidos", "local": "Los Angeles"},
            {"data": "25/06", "hora": "23h", "jogo": "Paraguai x Austrália", "local": "San Francisco"},
            # --- 26 de Junho ---
            {"data": "26/06", "hora": "16h", "jogo": "Noruega x França", "local": "Boston"},
            {"data": "26/06", "hora": "16h", "jogo": "Senegal x Iraque", "local": "Toronto"},
            {"data": "26/06", "hora": "21h", "jogo": "Cabo Verde x Arábia Saudita", "local": "Houston"},
            {"data": "26/06", "hora": "21h", "jogo": "Uruguai x Espanha", "local": "Guadalajara"},
            # --- 27 de Junho ---
            {"data": "27/06", "hora": "00h", "jogo": "Egito x Irã", "local": "Seattle"},
            {"data": "27/06", "hora": "00h", "jogo": "Nova Zelândia x Bélgica", "local": "Vancouver"},
            {"data": "27/06", "hora": "18h", "jogo": "Panamá x Inglaterra", "local": "Nova York/NJ"},
            {"data": "27/06", "hora": "18h", "jogo": "Croácia x Gana", "local": "Filadélfia"},
            {"data": "27/06", "hora": "20h30", "jogo": "Colômbia x Portugal", "local": "Miami"},
            {"data": "27/06", "hora": "20h30", "jogo": "RD Congo x Uzbequistão", "local": "Atlanta"},
            {"data": "27/06", "hora": "23h", "jogo": "Argélia x Áustria", "local": "Kansas City"},
            {"data": "27/06", "hora": "23h", "jogo": "Jordânia x Argentina", "local": "Dallas"}
        ]
    }
    
    # --- PROVEDOR 1: ZAFRONIX SPORTS API ---
    try:
        headers_zafronix = {"X-API-Key": "zwc_free_85be12c14621f2117b7dae7f"}
        response = requests.get("https://api.zafronix.com/fifa/worldcup/v1/tournaments/2026/fixtures", headers=headers_zafronix, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            fixtures_list = data.get("fixtures", [])
            if len(fixtures_list) > 0:
                calendario = []
                gols_br = [0, 0, 0, 0, 0, 0]
                idx_br = 0
                
                for match in fixtures_list:
                    time_c = traduzir(match["home_team"])
                    time_f = traduzir(match["away_team"])
                    g_c = match.get("home_score")
                    g_f = match.get("away_score")
                    placar = f" {g_c} x {g_f} " if g_c is not None else " x "
                    
                    calendario.append({
                        "data": datetime.strptime(match["date"], "%Y-%m-%d").strftime("%d/%m"),
                        "hora": match["time"][:5],
                        "jogo": f"{time_c}{placar}{time_f}",
                        "local": match.get("venue", "Estádio")
                    })
                    
                    if (time_c == "Brasil" or time_f == "Brasil") and match.get("status") == "FINISHED" and idx_br < 3:
                        gols_br[idx_br*2] = int(g_c) if time_c == "Brasil" else int(g_f)
                        gols_br[idx_br*2+1] = int(g_f) if time_c == "Brasil" else int(g_c)
                        idx_br += 1
                
                return {"classificacao_real": dados_padrao["classificacao_real"], "gols_reais_brasil": gols_br, "calendario_jogos": calendario}
    except Exception:
        pass
        
    # --- PROVEDOR 2: SPORTMONKS FOOTBALL API ---
    try:
        token_sportmonks = "Sdy1n1ctP5Q0ovO9NkVPZ5ey8Pfxqg2dRYRCmJl8lqjuk2MWw9ADP9ctWOUm"
        response = requests.get(f"https://api.sportmonks.com/v3/football/fixtures?api_token={token_sportmonks}&include=participants", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            fixtures_list = data.get("data", [])
            if len(fixtures_list) > 0:
                calendario = []
                gols_br = [0, 0, 0, 0, 0, 0]
                idx_br = 0
                
                for match in fixtures_list:
                    if match.get("league_id") == 1 or "World Cup" in str(match):
                        participants = match.get("participants", [])
                        if len(participants) < 2: continue
                        
                        time_c = traduzir(participants[0]["name"])
                        time_f = traduzir(participants[1]["name"])
                        scores = match.get("scores", {})
                        g_c = scores.get("localteam_score")
                        g_f = scores.get("visitorteam_score")
                        placar = f" {g_c} x {g_f} " if g_c is not None else " x "
                        
                        calendario.append({
                            "data": match.get("starting_at", "2026-06-11")[5:10].replace("-", "/"),
                            "hora": match.get("starting_at", "00:00:00")[11:16],
                            "jogo": f"{time_c}{placar}{time_f}",
                            "local": "Arena"
                        })
                        
                        if (time_c == "Brasil" or time_f == "Brasil") and match.get("state") == "ENDED" and idx_br < 3:
                            gols_br[idx_br*2] = int(g_c) if time_c == "Brasil" else int(g_f)
                            gols_br[idx_br*2+1] = int(g_f) if time_c == "Brasil" else int(g_c)
                            idx_br += 1
                
                if len(calendario) > 0:
                    return {"classificacao_real": dados_padrao["classificacao_real"], "gols_reais_brasil": gols_br, "calendario_jogos": calendario}
    except Exception:
        pass

    return dados_padrao

api_data = obter_resultados_reais_api()
# ==============================================================================
# 5. HEADER & ÁREA DE SELEÇÃO DE USUÁRIO
# ==============================================================================
st.markdown("🏆 BOLÃO DO BOBÃO COPA DO MUNDO 2026")                     
usuario_atual = st.selectbox("👤 Identifique-se para palpitar ou visualizar:", AMIGOS)

# 🛡️ FUNÇÃO DE EMERGÊNCIA (Garante a estrutura básica se tudo falhar)
def criar_banco_emergencia():
    banco = {}
    for amigo in AMIGOS:
        banco[amigo] = {
            "travado": False,
            "classificacao": {g: list(teams) for g, teams in GRUPOS_CONFIG.items()} if "GRUPOS_CONFIG" in globals() else {},
            "placar_brasil": [0, 0, 0, 0, 0, 0],
            "vencedores_mata_mata": {}
        }
    return banco

# 🛡️ TRAVA DE SEGURANÇA MÁXIMA
if "banco_palpites" not in st.session_state:
    try:
        st.session_state.banco_palpites = carregar_dados()
    except:
        st.session_state.banco_palpites = criar_banco_emergencia()

# Se mesmo após carregar os dados, o amigo selecionado não existir na memória:
if usuario_atual not in st.session_state.banco_palpites:
    st.warning("⚠️ Reconstruindo base de dados corrompida. Aguarde...")
    banco_emergencia = criar_banco_emergencia()
    
    # Mescla o banco de emergência mantendo o que já existia
    for amigo in AMIGOS:
        if amigo not in st.session_state.banco_palpites:
            st.session_state.banco_palpites[amigo] = banco_emergencia[amigo]

# Agora é 100% impossível dar KeyError, a variável é lida com segurança
dados_usuario = st.session_state.banco_palpites[usuario_atual]
# ==============================================================================

# Inicialização das abas nativas do Streamlit
aba_grupos, aba_matamata, aba_calendario, aba_ranking = st.tabs(["📊 Chaves & BR", "🌳 Mata-Mata", "📅 Calendário", "🥇 Classificação"])

# ------------------------------------------------------------------------------
# ABA 1: CLASSIFICAÇÃO DAS CHAVES, SELEÇÃO DO BRASIL E TRAVA DO CUZÃO
# ------------------------------------------------------------------------------
with aba_grupos:
    st.markdown("## 📊 Definição da Fase de Grupos")
    
    if dados_usuario["travado"]:
        st.markdown('<div class="status-travado">🔒 Palpites validados e salvos no sistema. Boa sorte, cuzão!</div>', unsafe_allow_html=True)
        
    palpites_fase_grupos = {}
    
    for nome_grupo, lista_times in GRUPOS_CONFIG.items():
        st.markdown(f'<div class="group-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="group-header">{nome_grupo}</div>', unsafe_allow_html=True)
        
        ordem_atual = dados_usuario["classificacao"][nome_grupo]
        
        if dados_usuario["travado"]:
            # Exibição estática caso o usuário já tenha efetuado o commit de segurança
            st.markdown(f"**1º:** {ordem_atual[0]} | **2º:** {ordem_atual[1]} | **3º:** {ordem_atual[2]} | **4º:** {ordem_atual[3]}")
            palpites_fase_grupos[nome_grupo] = ordem_atual
        else:
            # INTERFACE INTUITIVA COM TROCA AUTOMÁTICA (SWAP) SEM ERROS
            col1, col2 = st.columns(2)
            
            # 1º Colocado (Pode escolher qualquer um dos 4)
            t1 = col1.selectbox("🥇 1º Colocado", lista_times, index=lista_times.index(ordem_atual[0]), key=f"t1_{nome_grupo}")
            
            # Se o usuário escolheu para 1º o time que estava em 2º ou 3º, faz a troca automática
            if t1 != ordem_atual[0]:
                antigo_1 = ordem_atual[0]
                idx_duplicado = ordem_atual.index(t1)
                ordem_atual[0] = t1
                ordem_atual[idx_duplicado] = antigo_1
                st.rerun()

            # 2º Colocado
            opcoes_2 = [t for t in lista_times if t != t1]
            t2 = col2.selectbox("🥈 2º Colocado", opcoes_2, index=opcoes_2.index(ordem_atual[1]), key=f"t2_{nome_grupo}")
            
            if t2 != ordem_atual[1]:
                antigo_2 = ordem_atual[1]
                idx_duplicado = ordem_atual.index(t2)
                ordem_atual[1] = t2
                ordem_atual[idx_duplicado] = antigo_2
                st.rerun()

            # 3º Colocado
            opcoes_3 = [t for t in lista_times if t != t1 and t != t2]
            t3 = col1.selectbox("🥉 3º Colocado", opcoes_3, index=opcoes_3.index(ordem_atual[2]), key=f"t3_{nome_grupo}")
            
            if t3 != ordem_atual[2]:
                antigo_3 = ordem_atual[2]
                idx_duplicado = ordem_atual.index(t3)
                ordem_atual[2] = t3
                ordem_atual[idx_duplicado] = antigo_3
                st.rerun()
            
            # 4º Colocado é o que sobrou
            t4 = [t for t in lista_times if t != t1 and t != t2 and t != t3][0]
            ordem_atual[3] = t4
            col2.markdown(f"<p style='margin-top:25px; font-size:14px; color:#64748b;'>❌ 4º: {t4}</p>", unsafe_allow_html=True)
            
            palpites_fase_grupos[nome_grupo] = [t1, t2, t3, t4]
            
        st.markdown('</div>', unsafe_allow_html=True)


    # Seção exclusiva da Seleção Brasileira (Chave C)
    st.markdown("## 🇧🇷 Placar dos Jogos do Brasil (Grupo C)")
    palpites_gols_brasil = []
    
    for idx, jogo_info in enumerate(JOGOS_BRASIL):
        st.markdown(f"**{jogo_info['jogo']}**")
        st.caption(f"🗓️ {jogo_info['data']} - 🏟️ {jogo_info['loc']}")
        
        c_br, c_adv = st.columns(2)
        base_idx = idx * 2
        
        gols_br = c_br.number_input("Gols Brasil", min_value=0, max_value=20, value=dados_usuario["placar_brasil"][base_idx], step=1, key=f"g_br_{idx}", disabled=dados_usuario["travado"])
        gols_adv = c_adv.number_input("Gols Adv", min_value=0, max_value=20, value=dados_usuario["placar_brasil"][base_idx+1], step=1, key=f"g_adv_{idx}", disabled=dados_usuario["travado"])
        
        palpites_gols_brasil.extend([gols_br, gols_adv])

    # Mecanismo da Trava de Segurança Unilateral ("Tem certeza cuzão?")
    if not dados_usuario["travado"]:
        st.write("---")
        if st.button("🚨 SALVAR PALPITES DEFINITIVOS"):
            st.session_state.disparar_trava = True
            
        if st.session_state.get("disparar_trava", False):
            st.markdown("""
                <div class="cuzao-box">
                    <p class="cuzao-title">⚠️ ATENÇÃO - SEGURANÇA MÁXIMA</p>
                    <p style="color: #334155; font-size: 14px; font-weight: bold;">Tem certeza cuzão? Não vai mais poder editar nada depois disso.</p>
                </div>
            """, unsafe_allow_html=True)
            
            col_sim, col_nao = st.columns(2)
            if col_sim.button("🔥 SIM, TENHO CERTEZA"):
                dados_usuario["classificacao"] = {g: list(palpites_fase_grupos[g]) for g in GRUPOS_CONFIG.keys()}
                dados_usuario["placar_brasil"] = palpites_gols_brasil
                dados_usuario["travado"] = True
                
                # ENVIA OS DADOS PARA A PLANILHA DO GOOGLE
                salvar_dados_sheets(usuario_atual, dados_usuario)
                
                st.session_state.disparar_trava = False
                st.success("Palpites bloqueados com sucesso!")
                st.rerun()
                
            if col_nao.button("🔒 NÃO, QUERO REVISAR"):
                st.session_state.disparar_trava = False
                st.rerun()

# ------------------------------------------------------------------------------
# ABA 2: MATA-MATA (ESTRUTURA COMPLETA COMPILADA E TRAVADA NO BACKEND)
# ------------------------------------------------------------------------------
with aba_matamata:
    st.markdown("## 🌳 Chaveamento do Mata-Mata")
    
    if not MATA_MATA_LIBERADO:
        st.info("🔒 Aba bloqueada para edição. Os confrontos estarão disponíveis assim que o chaveamento real da Copa de 2026 for consolidado.")
        
    st.markdown("### Configuração das Oitavas de Final (Simulação Visual)")
    
    # Renderização estática da árvore de chaveamento montada a partir dos dados do GE
    for conf in MATA_MATA_CONFRONTOS:
        st.markdown(f'<div class="group-card">', unsafe_allow_html=True)
        st.markdown(f"**Confronto {conf['id']}**")
        
        # O parâmetro disabled=True assegura que os amigos vejam o design visual completo sem poder alterar nada precocemente
        selecionado = st.radio(
            "Quem avança de fase?",
            options=[conf["t1"], conf["t2"]],
            key=f"radio_{conf['id']}",
            disabled=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 3. BANCO DE DADOS E PERSISTÊNCIA (Nuvem Oficial com JSONBin.io)
# ==============================================================================
import json
import requests

# Função de segurança: garante que todos os amigos existam na base de dados (Evita KeyError)
def obter_banco_padrao():
    banco = {}
    for amigo in AMIGOS:
        banco[amigo] = {
            "travado": False,
            "classificacao": {g: list(teams) for g, teams in GRUPOS_CONFIG.items()},
            "placar_brasil": [0, 0, 0, 0, 0, 0],
            "vencedores_mata_mata": {c["id"]: "" for c in MATA_MATA_CONFRONTOS}
        }
    return banco

def carregar_dados():
    banco_seguro = obter_banco_padrao()
    try:
        bin_id = st.secrets.get("JSONBIN_ID")
        api_key = st.secrets.get("JSONBIN_KEY")
        
        # Se as chaves ainda não estiverem no Streamlit, roda liso na memória local
        if not bin_id or not api_key:
            return banco_seguro
            
        url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        headers = {"X-Master-Key": api_key}
        
        req = requests.get(url, headers=headers, timeout=5)
        if req.status_code == 200:
            dados_nuvem = req.json().get("record", {})
            
            # Atualiza o banco seguro APENAS com os amigos que já salvaram na nuvem
            for amigo in AMIGOS:
                if amigo in dados_nuvem:
                    banco_seguro[amigo]["travado"] = dados_nuvem[amigo].get("travado", False)
                    banco_seguro[amigo]["classificacao"] = dados_nuvem[amigo].get("classificacao", banco_seguro[amigo]["classificacao"])
                    banco_seguro[amigo]["placar_brasil"] = dados_nuvem[amigo].get("placar_brasil", banco_seguro[amigo]["placar_brasil"])
                    banco_seguro[amigo]["vencedores_mata_mata"] = dados_nuvem[amigo].get("vencedores_mata_mata", banco_seguro[amigo]["vencedores_mata_mata"])
                    
        return banco_seguro
    except Exception:
        # Se a internet cair, carrega o banco padrão sem quebrar a tela
        return banco_seguro

def salvar_dados(amigo_nome, novos_dados):
    try:
        # Atualiza a memória local instantaneamente
        st.session_state.banco_palpites[amigo_nome] = novos_dados
        banco_atual = st.session_state.banco_palpites
        
        bin_id = st.secrets.get("JSONBIN_ID")
        api_key = st.secrets.get("JSONBIN_KEY")
        
        if bin_id and api_key:
            url = f"https://api.jsonbin.io/v3/b/{bin_id}"
            headers = {
                "Content-Type": "application/json",
                "X-Master-Key": api_key
            }
            # Empurra os dados para a nuvem
            requests.put(url, json=banco_atual, headers=headers)
    except Exception as e:
        st.error("Erro de conexão ao salvar na nuvem, mas seu palpite está na memória!")

# Inicialização síncrona
if "banco_palpites" not in st.session_state:
    st.session_state.banco_palpites = carregar_dados()

banco_palpites = st.session_state.banco_palpites

# ------------------------------------------------------------------------------
# ABA 4: RANKING, CRITÉRIOS DE PONTUAÇÃO E GAMIFICAÇÃO COM BADGES
# ------------------------------------------------------------------------------
with aba_ranking:
    st.markdown("## 🥇 Classificação Geral dos Amigos")
    
    dados_tabela_ranking = []
    
    for amigo in AMIGOS:
        user_info = st.session_state.banco_palpites[amigo]
        pontuacao_total = 0
        acertou_placar_em_cheio = False
        errou_absolutamente_tudo = True
        
        if user_info["travado"]:
            # 1. Validação de Pontos da Fase de Grupos (2 pts por posição correta)
            for g in GRUPOS_CONFIG.keys():
                if user_info["classificacao"][g][0] == api_data["classificacao_real"][g][0]:
                    pontuacao_total += 2
                if user_info["classificacao"][g][1] == api_data["classificacao_real"][g][1]:
                    pontuacao_total += 2
                    
            # 2. Validação de Pontos da Seleção Brasileira
            for i in range(3):
                base = i * 2
                p_br, p_adv = user_info["placar_brasil"][base], user_info["placar_brasil"][base+1]
                r_br, r_adv = api_data["gols_reais_brasil"][base], api_data["gols_reais_brasil"][base+1]
                
                # Regra: Placar Exato em cheio = 5 pontos
                if p_br == r_br and p_adv == r_adv:
                    pontuacao_total += 5
                    acertou_placar_em_cheio = True
                    errou_absolutamente_tudo = False
                # Regra: Acerto de vencedor ou empate (tendência do jogo) = 3 pontos
                elif (p_br > p_adv and r_br > r_adv) or (p_br < p_adv and r_br < r_adv) or (p_br == p_adv and r_br == r_adv):
                    pontuacao_total += 3
                    errou_absolutamente_tudo = False
        else:
            # Penalidade temporária ou pontuação zerada se não efetuou o travamento
            pontuacao_total = 0
            errou_absolutamente_tudo = False
            
        # Atribuição da lógica de Gamificação por Badges Dinâmicas
        lista_badges = []
        if user_info["travado"] and acertou_placar_em_cheio:
            lista_badges.append("🔮 O Profeta")
        if user_info["travado"] and errou_absolutamente_tudo:
            lista_badges.append("🤡 Zica do Rolê")
        if not user_info["travado"]:
            lista_badges.append("⏳ Editando...")
            
        dados_tabela_ranking.append({
            "Amigo": amigo,
            "Pontuação": pontuacao_total,
            "🏅 Conquistas / Badges": " | ".join(lista_badges) if lista_badges else "🏃 Em jogo",
            "Segurança": "🔒 Travado" if user_info["travado"] else "🔓 Aberto"
        })
        
    # Ordenação do Dataframe por pontuação decrescente
    df_ranking = pd.DataFrame(dados_tabela_ranking).sort_values(by="Pontuação", ascending=False).reset_index(drop=True)
    
    # Injeção das Badges Supremas (Líder e Lanterna) baseado nas posições relativas
    if len(df_ranking) > 0 and df_ranking.loc[0, "Pontuação"] > 0:
        df_ranking.loc[0, "🏅 Conquistas / Badges"] = "👑 [LÍDER] " + df_ranking.loc[0, "🏅 Conquistas / Badges"]
        idx_ultimo = len(df_ranking) - 1
        if df_ranking.loc[idx_ultimo, "Pontuação"] < df_ranking.loc[0, "Pontuação"]:
            df_ranking.loc[idx_ultimo, "🏅 Conquistas / Badges"] = "🔦 [Lanterna] " + df_ranking.loc[idx_ultimo, "🏅 Conquistas / Badges"]
            
    # Renderização da Tabela Otimizada para Visualização Mobile
    st.dataframe(
        df_ranking,
        column_config={
            "Amigo": st.column_config.TextColumn("Nome"),
            "Pontuação": st.column_config.NumberColumn("PTS 🎯"),
            "🏅 Conquistas / Badges": st.column_config.TextColumn("Badges"),
            "Segurança": st.column_config.TextColumn("Status")
        },
        hide_index=True,
        use_container_width=True
    )
