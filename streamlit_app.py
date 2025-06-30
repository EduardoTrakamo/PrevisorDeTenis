import streamlit as st

def prever_mercado_gols(
    minuto,
    placar_a, placar_b,
    finalizacoes_a, finalizacoes_b,
    chutes_alvo_a, chutes_alvo_b,
    xg_a, xg_b,
    ataques_perigosos_a, ataques_perigosos_b,
    posse_a, posse_b
):
    gols_total = placar_a + placar_b

    # Intensidade ofensiva
    intensidade_a = finalizacoes_a + chutes_alvo_a * 2 + ataques_perigosos_a * 0.5 + xg_a * 10
    intensidade_b = finalizacoes_b + chutes_alvo_b * 2 + ataques_perigosos_b * 0.5 + xg_b * 10
    intensidade_total = (intensidade_a + intensidade_b) / (minuto + 1)

    # Estimativas de probabilidade para próximos gols
    prob_mais_1_gol = min(1.0, intensidade_total / 3.0)
    prob_mais_2_gols = min(1.0, intensidade_total / 4.5)

    # Quem deve marcar o próximo gol
    proporcao_a = intensidade_a / (intensidade_a + intensidade_b) if (intensidade_a + intensidade_b) > 0 else 0.5
    proporcao_b = 1 - proporcao_a

    return {
        "gols_total": gols_total,
        "proximo_mercado_over": f"Over {gols_total + 0.5}",
        "proximo_mercado_under": f"Under {gols_total + 0.5}",
        "prob_mais_1_gol": prob_mais_1_gol,
        "prob_mais_2_gols": prob_mais_2_gols,
        "proximo_gol_a": proporcao_a,
        "proximo_gol_b": proporcao_b,
        "intensidade_a": intensidade_a,
        "intensidade_b": intensidade_b,
        "intensidade_total": intensidade_total
    }

# Interface Streamlit
st.set_page_config(page_title="Bot de Gols ao Vivo", layout="centered")
st.title("⚽ Bot de Gols ao Vivo")

st.header("📋 Informações da Partida")
minuto = st.slider("Minuto de jogo", 1, 90, 30)
placar_a = st.number_input("Gols Time A", min_value=0)
placar_b = st.number_input("Gols Time B", min_value=0)

st.header("📊 Estatísticas do Time A")
finalizacoes_a = st.number_input("Finalizações Time A", min_value=0)
chutes_alvo_a = st.number_input("Chutes no Alvo Time A", min_value=0)
xg_a = st.number_input("xG Time A", min_value=0.0)
ataques_perigosos_a = st.number_input("Ataques Perigosos Time A", min_value=0)
posse_a = st.slider("Posse de Bola Time A (%)", 0, 100, 50)

st.header("📊 Estatísticas do Time B")
finalizacoes_b = st.number_input("Finalizações Time B", min_value=0)
chutes_alvo_b = st.number_input("Chutes no Alvo Time B", min_value=0)
xg_b = st.number_input("xG Time B", min_value=0.0)
ataques_perigosos_b = st.number_input("Ataques Perigosos Time B", min_value=0)
posse_b = 100 - posse_a  # automático

if st.button("🔍 Analisar Jogo"):
    resultado = prever_mercado_gols(
        minuto, placar_a, placar_b,
        finalizacoes_a, finalizacoes_b,
        chutes_alvo_a, chutes_alvo_b,
        xg_a, xg_b,
        ataques_perigosos_a, ataques_perigosos_b,
        posse_a, posse_b
    )

    st.subheader("📈 Resultados da Análise")

    st.markdown(f"**🔥 Intensidade Time A:** `{resultado['intensidade_a']:.2f}`")
    st.markdown(f"**🔥 Intensidade Time B:** `{resultado['intensidade_b']:.2f}`")
    st.markdown(f"**⚡ Intensidade Total:** `{resultado['intensidade_total']:.2f}`")

    st.markdown(f"**🎯 Placar atual:** `{placar_a}x{placar_b}` | Total de Gols: `{resultado['gols_total']}`")

    st.markdown(f"**📊 Próximo mercado de gols:** `{resultado['proximo_mercado_over']}` ou `{resultado['proximo_mercado_under']}`")

    st.markdown(f"**📈 Chance de mais 1 gol:** `{resultado['prob_mais_1_gol'] * 100:.1f}%`")
    st.markdown(f"**📈 Chance de mais 2 gols:** `{resultado['prob_mais_2_gols'] * 100:.1f}%`")

    if resultado['prob_mais_1_gol'] > 0.75:
        st.success("✅ Alta chance de mais 1 gol — avaliar entrada no mercado de gols!")
    elif resultado['prob_mais_1_gol'] < 0.40:
        st.info("🧊 Baixa chance de mais 1 gol — jogo controlado.")

    if resultado['prob_mais_2_gols'] > 0.70:
        st.success("✅ Boa chance de mais 2 gols — avaliar mercado de Over avançado!")
    elif resultado['prob_mais_2_gols'] < 0.35:
        st.info("🧊 Baixa chance de mais 2 gols — tendência de Under.")

    st.markdown(f"**⚽ Próximo gol:**")
    st.markdown(f"- Time A: `{resultado['proximo_gol_a'] * 100:.1f}%`")
    st.markdown(f"- Time B: `{resultado['proximo_gol_b'] * 100:.1f}%`")
