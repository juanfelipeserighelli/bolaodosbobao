import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ==============================================================================
# 1. CONFIGURAÇÕES DA PÁGINA (Design Premium Otimizado para Chrome Mobile)
# ==============================================================================
st.set_page_config(
    page_title="Bolão Copa 2026",
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
# 3. BANCO DE DADOS E PERSISTÊNCIA (Session State + Prontidão para Google Sheets)
# ==============================================================================
if "banco_palpites" not in st.session_state:
    st.session_state.banco_palpites = {}
    for amigo in AMIGOS:
        st.session_state.banco_palpites[amigo] = {
            "travado": False,
            "classificacao": {g: list(teams) for g, teams in GRUPOS_CONFIG.items()},
            "terceiros": [],
            "placar_brasil": [0, 0, 0, 0, 0, 0], # Armazena gols sequencialmente: [br1, adv1, br2, adv2...]
            "vencedores_mata_mata": {c["id"]: "" for c in MATA_MATA_CONFRONTOS}
        }

# ==============================================================================
# 4. CONSUMO DE RESULTADOS REAIS SIMULANDO A API (Processado a cada refresh)
# ==============================================================================
@st.cache_data(ttl=5)  # Atualização dinâmica em tempo real a cada requisição
def obter_resultados_reais_api():
    # Estrutura espelho contendo os gabaritos oficiais calculados dinamicamente pela API
    return {
        "classificacao_real": {g: list(teams) for g, teams in GRUPOS_CONFIG.items()}, # Simulando resultados idênticos
        "gols_reais_brasil": [3, 1, 2, 0, 1, 1], # Gabarito real dos placares [BR x Marrocos, BR x Haiti...]
        "calendario_jogos": [
            {"data": "11 de junho", "hora": "16h", "jogo": "México x África do Sul", "local": "Cidade do México"},
            {"data": "11 de junho", "hora": "23h", "jogo": "República da Coreia x Tchéquia", "local": "Guadalajara"},
            {"data": "12 de junho", "hora": "16h", "jogo": "Canadá x Bósnia e Herzegovina", "local": "Toronto"},
            {"data": "12 de junho", "hora": "22h", "jogo": "Estados Unidos x Paraguai", "local": "Los Angeles"},
            {"data": "13 de junho", "hora": "16h", "jogo": "Catar x Suíça", "local": "San Francisco"},
            {"data": "13 de junho", "hora": "19h", "jogo": "Brasil x Marrocos", "local": "Nova York/Nova Jersey"},
            {"data": "13 de junho", "hora": "22h", "jogo": "Haiti x Escócia", "local": "Boston"}
        ]
    }

api_data = obter_resultados_reais_api()

# ==============================================================================
# 5. HEADER & ÁREA DE SELEÇÃO DE USUÁRIO
# ==============================================================================
st.markdown("<h1>🏆 BOLÃO COPA DO MUNDO 2026</h1>")
usuario_atual = st.selectbox("👤 Identifique-se para palpitar ou visualizar:", AMIGOS)
dados_usuario = st.session_state.banco_palpites[usuario_atual]

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
                dados_usuario["classificacao"] = palpites_fase_grupos
                dados_usuario["placar_brasil"] = palpites_gols_brasil
                dados_usuario["travado"] = True
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

# ------------------------------------------------------------------------------
# ABA 3: CALENDÁRIO DIÁRIO COMPILADO VIA API DE DADOS
# ------------------------------------------------------------------------------
with aba_calendario:
    st.markdown("## 📅 Cronograma Oficial de Jogos")
    st.caption("Resultados atualizados de forma síncrona a cada requisição de página.")
    st.write("---")
    
    # Agrupamento e exibição linear por data para leitura fluida no Android Chrome
    for jogo in api_data["calendario_jogos"]:
        col_meta, col_partida = st.columns([1, 2])
        with col_meta:
            st.markdown(f"📅 **{jogo['data']}**")
            st.caption(f"⏰ {jogo['hora']}")
        with col_partida:
            st.markdown(f"🏟️ *{jogo['local']}*")
            st.markdown(f"👉 **{jogo['jogo']}**")
        st.markdown("<hr style='margin: 8px 0; opacity: 0.2;'>", unsafe_allow_html=True)

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
