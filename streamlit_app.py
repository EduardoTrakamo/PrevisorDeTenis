import streamlit as st

st.set_page_config(page_title="Previsor de Set de Tênis", layout="centered")

st.title("🎾 Previsor de Set - Tênis Ao Vivo")

stats_labels = [
    "1º Serviço (%)", "Pts Ganhos no 1º Serviço (%)",
    "2º Serviço (%)", "Pts Ganhos no 2º Serviço (%)",
    "Break Points Convertidos (%)", "Aces", "Duplas Faltas",
    "Games Vencidos no Set"
]
weights = [1.2, 1.5, 1.0, 1.3, 1.4, 1.0, -1.2, 1.6]

st.markdown("#### 📋 Estatísticas dos Jogadores")

col1, col2 = st.columns(2)
a_vals = []
b_vals = []

with col1:
    st.markdown("**Jogador A**")
    for stat in stats_labels:
        val = st.number_input(f"A - {stat}", value=0.0, format="%.1f", key=f"a_{stat}")
        a_vals.append(val)

with col2:
    st.markdown("**Jogador B**")
    for stat in stats_labels:
        val = st.number_input(f"B - {stat}", value=0.0, format="%.1f", key=f"b_{stat}")
        b_vals.append(val)

st.divider()

linha = st.number_input("📏 Linha Over/Under (Games)", value=22.5, step=0.5)
odd_over = st.number_input("🔼 Odd Over", value=1.80, step=0.01)
odd_under = st.number_input("🔽 Odd Under", value=1.80, step=0.01)

st.divider()

if st.button("🔍 Analisar"):
    try:
        weighted_a = sum([(a - b) * w for a, b, w in zip(a_vals, b_vals, weights)])
        prob_a = max(0, min(100, 50 + weighted_a * 2))
        prob_b = 100 - prob_a

        eff_a = (a_vals[1] + a_vals[3]) / 2
        eff_b = (b_vals[1] + b_vals[3]) / 2
        total_games = a_vals[7] + b_vals[7]

        dominio_b = (b_vals[1] - a_vals[1]) + (b_vals[3] - a_vals[3]) + (b_vals[4] - a_vals[4]) + (b_vals[7] - a_vals[7])
        estimativa_fechamento = total_games + (2 if dominio_b > 8 else 3 if dominio_b > 3 else 4)

        sugestao = "UNDER" if estimativa_fechamento < linha else "OVER"

        st.markdown(f"""
        ### 📊 Resultado da Análise

        **Probabilidades de vencer o SET atual:**
        - 🟦 Jogador A: `{prob_a:.1f}%`
        - 🟥 Jogador B: `{prob_b:.1f}%`

        **Probabilidades do JOGO final:**
        - A: `{prob_a + 3:.1f}%`
        - B: `{prob_b - 3:.1f}%`

        **Total de games jogados:** {int(total_games)}

        **Eficiência média do saque:**
        - A: `{eff_a:.1f}%`
        - B: `{eff_b:.1f}%`

        **Estimativa de fechamento do set:** `{estimativa_fechamento:.1f}` games  
        **Linha fornecida:** `{linha}`

        ✅ **Sugestão:** Apostar em **{sugestao} {linha}**
        """)
    except Exception as e:
        st.error(f"Erro ao calcular: {e}")
