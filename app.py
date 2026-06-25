import streamlit as st
import math

st.set_page_config(page_title="Calculateur de position", layout="wide")

st.title("📊 Calculateur de taille de position")

st.markdown("Calcule rapidement combien d’actions prendre selon ton risque.")

# =========================
# INPUTS
# =========================
col1, col2 = st.columns(2)

with col1:
    account_size = st.number_input("Capital du compte ($)", min_value=0.0, value=25000.0, step=500.0)
    risk_mode = st.selectbox("Mode de risque", ["Pourcentage", "Montant fixe"])
    
    if risk_mode == "Pourcentage":
        risk_percent = st.number_input("Risque par trade (%)", min_value=0.0, value=1.0, step=0.1)
        risk_amount = account_size * (risk_percent / 100)
    else:
        risk_amount = st.number_input("Risque par trade ($)", min_value=0.0, value=250.0, step=25.0)

with col2:
    direction = st.selectbox("Type de trade", ["Long", "Short"])
    entry_price = st.number_input("Prix d’entrée ($)", min_value=0.0, value=50.0, step=0.01)
    stop_price = st.number_input("Prix du stop ($)", min_value=0.0, value=48.0, step=0.01)
    target_price = st.number_input("Prix cible / target ($)", min_value=0.0, value=54.0, step=0.01)

# =========================
# CALCULS
# =========================
if direction == "Long":
    risk_per_share = entry_price - stop_price
    reward_per_share = target_price - entry_price
else:
    risk_per_share = stop_price - entry_price
    reward_per_share = entry_price - target_price

# =========================
# OUTPUT
# =========================
st.divider()

if risk_per_share <= 0:
    st.error("⚠️ Le stop n’est pas valide pour ce type de trade.")
else:
    shares = math.floor(risk_amount / risk_per_share)
    position_value = shares * entry_price
    max_loss = shares * risk_per_share
    potential_gain = shares * reward_per_share if reward_per_share > 0 else 0
    rr = reward_per_share / risk_per_share if reward_per_share > 0 else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Risque total", f"${risk_amount:,.2f}")
    c2.metric("Risque / action", f"${risk_per_share:.2f}")
    c3.metric("Nombre d’actions", f"{shares:,}")
    c4.metric("Valeur position", f"${position_value:,.2f}")

    st.subheader("📈 Résumé du trade")

    st.write(f"**Type :** {direction}")
    st.write(f"**Entrée :** ${entry_price:.2f}")
    st.write(f"**Stop :** ${stop_price:.2f}")
    st.write(f"**Target :** ${target_price:.2f}")
    st.write(f"**Perte maximale réelle :** ${max_loss:,.2f}")
    st.write(f"**Gain potentiel :** ${potential_gain:,.2f}")
    st.write(f"**Ratio R:R :** {rr:.2f}")

    if rr < 1:
        st.warning("⚠️ Ratio risque/rendement faible.")
    elif rr >= 2:
        st.success("✅ Excellent ratio risque/rendement.")
    else:
        st.info("ℹ️ Ratio acceptable.")

    if position_value > account_size:
        st.warning("⚠️ La valeur de la position dépasse ton capital disponible.")
