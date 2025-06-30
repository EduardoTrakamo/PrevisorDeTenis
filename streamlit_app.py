import streamlit as st

def prever_mercado_gols( minuto, placar_a, placar_b, odd_over15, odd_over25, finalizacoes_a, finalizacoes_b, chutes_alvo_a, chutes_alvo_b, xg_a, xg_b, ataques_perigosos_a, ataques_perigosos_b, posse_a, posse_b ): gols_total = placar_a + placar_b

# Intensidade ofensiva
intensidade_a = finalizacoes_a + chutes_alvo_a*2 + ataques_perigosos_a*0.5 + xg_a*10
intensidade_b = finalizacoes_b + chutes_alvo_b*2 + ataques_perigosos_b*0.5 + xg_b*10
intensidade_total = (intensidade_a + intensidade_b) / (minuto + 1)

# Estimativa de probabilidade empírica
prob_over15 = min(1.0, (intensidade_total / 3.0))
prob_over25 = min(1.0, (intensidade_total / 4.5))

# EV (valor esperado)
ev_over15 = (prob_over15 * odd_over15) - 1
ev_over25 = (prob_over25 * odd_over25) - 1

# Quem deve marcar o próximo gol
proporcao_a = intensidade_a / (intensidade_a + intensidade_b) if (intensidade_a + intensidade_b) > 0 else 0.5
proporcao_b = 1 - proporcao_a

return {
    "prob_over15": prob_over15,
    "prob_over25": prob_over25,
    "ev_over15": ev_over15,
    "ev_over25": ev_over25,
    "proximo_gol_a": proporcao_a,
    "proximo_gol_b": proporcao_b,
    "intensidade_a": intensidade_a,
    "intensidade_b": intensidade_b,
    "intensidade_total": intensidade_total
}

st.title("Bot de Gols ao Vivo - Futebol")

st.header("Informações da Partida") minuto = st.slider("Minuto de jogo", 1, 90, 30) placar_a = st.number_input("Gols Time A", 0) placar_b = st.number_input("Gols Time B", 0)

st.header("Odds do Mercado") odd_over15 = st.number_input("Odd Over 1.5", 1.01) odd_over25 = st.number_input("Odd Over 2.5", 1.01)

st.header("Estatísticas do Time A") finalizacoes_a = st.number_input("Finalizações Time A", 0) chutes_alvo_a = st.number_input("Chutes no Alvo Time A", 0) xg_a = st.number_input("xG Time A", 0.0) ataques_perigosos_a = st.number_input("Ataques Perigosos Time A", 0) posse_a = st.slider("Posse de Bola Time A (%)", 0, 100, 50)

st.header("Estatísticas do Time B") finalizacoes_b = st.number_input("Finalizações Time B", 0) chutes_alvo_b = st.number_input("Chutes no Alvo Time B", 0) xg_b = st.number_input("xG Time B", 0.0) ataques_perigosos_b = st.number_input("Ataques Perigosos Time B", 0) posse_b = 100 - posse_a

if st.button("Analisar Jogo"): resultado = prever_mercado_gols( minuto, placar_a, placar_b, odd_over15, odd_over25, finalizacoes_a, finalizacoes_b, chutes_alvo_a, chutes_alvo_b, xg_a, xg_b, ataques_perigosos_a, ataques_perigosos_b, posse_a, posse_b )

st.subheader("Resultados da Análise")
st.write(f"🔥 Intensidade Time A: {resultado['intensidade_a']:.2f}")
st.write(f"🔥 Intensidade Time B: {resultado['intensidade_b']:.2f}")
st.write(f"⚡ Intensidade Total: {resultado['intensidade_total']:.2f}")

st.write(f"\n🎯 Over 1.5 → Prob: {resultado['prob_over15']*100:.1f}% | EV: {resultado['ev_over15']:.2f}")
st.write(f"🎯 Over 2.5 → Prob: {resultado['prob_over25']*100:.1f}% | EV: {resultado['ev_over25']:.2f}")

if resultado['ev_over15'] > 0:
    st.success("✅ Over 1.5 tem valor! Possível entrada.")
else:
    st.warning("❌ Over 1.5 sem valor no momento.")

if resultado['ev_over25'] > 0:
    st.success("✅ Over 2.5 tem valor!")
else:
    st.warning("❌ Over 2.5 não compensa.")

st.write(f"\n⚽ Próximo gol - Time A: {resultado['proximo_gol_a']*100:.1f}% | Time B: {resultado['proximo_gol_b']*100:.1f}%")

