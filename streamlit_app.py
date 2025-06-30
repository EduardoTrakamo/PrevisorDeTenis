import streamlit as st

def prever_gols(
    minuto, placar_a, placar_b,
    finalizacoes_a, finalizacoes_b,
    chutes_alvo_a, chutes_alvo_b,
    xg_a, xg_b,
    ataques_perigosos_a, ataques_perigosos_b,
    posse_a, posse_b
):
    gols_total = placar_a + placar_b

    # Intensidade ofensiva por time
    intensidade_a = finalizacoes_a + chutes_alvo_a * 2 + ataques_perigosos_a * 0.5 + xg_a * 10
    intensidade_b = finalizacoes_b + chutes_alvo_b * 2 + ataques_perigosos_b * 0.5 + xg_b * 10
    intensidade_total = intensidade_a + intensidade_b

    # Ajuste de divisor por tempo de jogo
    if minuto <= 15:
        divisor = 20
    elif minuto <= 30:
        divisor = minuto + 3
    else:
        divisor = minuto

    # Probabilidade estimada de mais 1 e mais 2 gols
    taxa_intensidade = intensidade_total / divisor
    prob_mais_1 = min(1.0, taxa_intensidade / 1.5)
    prob_mais_2 = min(1.0, taxa_intensidade / 2.5)

    proximo_mercado = gols_total + 0.5

    # Quem marca o próximo gol
    soma_intensidade = intensidade_a + intensidade_b
    if soma_intensidade > 0:
        pct_a = intensidade_a / soma_intensidade
        pct_b = 1 - pct_a
    else:
        pct_a, pct_b = 0.5, 0.5

    return {
        "intensidade_a": intensidade_a,
        "intensidade_b": intensidade_b,
        "taxa": taxa_intensidade,
        "prob_mais_1": prob_mais_1,
        "prob_mais_2": prob_mais_2,
        "proximo_mercado": proximo_mercado,
        "proximo_gol_a": pct_a,
        "proximo_gol_b": pct_b,
        "gols_total": gols_total
    }

# Interface
st.set_page_config("Bot de Gols ao Vivo", layout="centered")
st.title("⚽ Bot Inteligente de Gols ao Vivo")

st.header("📋 Informações da Partida")
minuto = st.slider("Minuto de jogo", 1, 90, 13)
placar_a = st.number_input("Gols Time A", 0)
placar_b = st.number_input("Gols Time B", 0)

st.header("📊 Estatísticas do Time A")
finalizacoes_a = st.number_input("Finalizações", 0)
chutes_alvo_a = st.number_input("Chutes no Alvo", 0)
xg_a = st.number_input("xG", 0.0)
ataques_perigosos_a = st.number_input("Ataques Perigosos", 0)
posse_a = st.slider("Posse de Bola (%)", 0, 100, 50)

st.header("📊 Estatísticas do Time B")
finalizacoes_b = st.number_input("Finalizações ", 0)
chutes_alvo_b = st.number_input("Chutes no Alvo ", 0)
xg_b = st.number_input("xG ", 0.0)
ataques_perigosos_b = st.number_input("Ataques Perigosos ", 0)
posse_b = 100 - posse_a

if st.button("🔍 Analisar"):
    r = prever_gols(
        minuto, placar_a, placar_b,
        finalizacoes_a, finalizacoes_b,
        chutes_alvo_a, chutes_alvo_b,
        xg_a, xg_b,
        ataques_perigosos_a, ataques_perigosos_b,
        posse_a, posse_b
    )

    st.subheader("📈 Análise")
    st.markdown(f"**🔢 Total de Gols:** `{r['gols_total']}`")
    st.markdown(f"**📊 Mercado Atual:** Over/Under `{r['proximo_mercado']}`")
    st.markdown(f"**🔥 Intensidade Total:** `{r['taxa']:.2f}`")
    st.markdown(f"**🔮 Prob. Mais 1 Gol:** `{r['prob_mais_1']*100:.1f}%`")
    st.markdown(f"**🔮 Prob. Mais 2 Gols:** `{r['prob_mais_2']*100:.1f}%`")

    if r['prob_mais_1'] > 0.75:
        st.success("✅ Alta chance de mais 1 gol — ótima entrada no Over!")
    elif r['prob_mais_1'] > 0.55:
        st.info("🟡 Probabilidade razoável — acompanhar o jogo.")
    else:
        st.warning("🧊 Jogo controlado — tendência de Under.")

    if r['prob_mais_2'] > 0.7:
        st.success("✅ Pressão clara — considerar Over mais agressivo.")
    elif r['prob_mais_2'] < 0.4:
        st.info("📉 Baixa chance de mais 2 gols — Under avançado possível.")

    st.markdown("**⚽ Quem deve marcar o próximo gol:**")
    st.markdown(f"- Time A: `{r['proximo_gol_a']*100:.1f}%`")
    st.markdown(f"- Time B: `{r['proximo_gol_b']*100:.1f}%`")

