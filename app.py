import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="TEA Trading Toolkit", layout="wide")

st.title("📊 TEA Trading Toolkit")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Position Size",
    "Scénarios Stops",
    "Targets en R",
    "Risque Journalier",
    "Kelly"
])

# =========================
# TAB 1 — POSITION SIZE
# =========================
with tab1:
    st.header("📌 Calculateur de position")

    col1, col2 = st.columns(2)

    with col1:
        account_size = st.number_input("Capital du compte ($)", value=25000.0, step=500.0)
        risk_percent = st.number_input("Risque par trade (%)", value=1.0, step=0.1)
        risk_amount = account_size * risk_percent / 100

    with col2:
    direction = st.selectbox("Direction", ["Long", "Short"])
    entry = st.number_input("Prix d'entrée", value=50.0, step=0.01)
    stop_risk_pct = st.number_input("Distance du stop (%)", value=2.0, step=0.1)

    if direction == "Long":
        stop = entry * (1 - stop_risk_pct / 100)
    else:
        stop = entry * (1 + stop_risk_pct / 100)

    st.metric("Stop calculé", f"${stop:.2f}")

# =========================
# TAB 2 — SCÉNARIOS STOPS
# =========================
with tab2:
    st.header("📉 Scénarios de stops")

    account = st.number_input("Capital ($)", value=25000.0, step=500.0, key="sc_account")
    risk_pct = st.number_input("Risque (%)", value=1.0, step=0.1, key="sc_risk")
    entry_sc = st.number_input("Entrée", value=50.0, step=0.01, key="sc_entry")

    stops_text = st.text_area(
        "Stops à tester, un par ligne",
        "49.80\n49.50\n49.00\n48.50"
    )

    risk_dollars = account * risk_pct / 100
    rows = []

    for s in stops_text.splitlines():
        try:
            stop_val = float(s.strip())
            risk_ps = abs(entry_sc - stop_val)

            if risk_ps > 0:
                shares = math.floor(risk_dollars / risk_ps)
                rows.append({
                    "Stop": stop_val,
                    "Risque/action": round(risk_ps, 2),
                    "Actions": shares,
                    "Valeur position": round(shares * entry_sc, 2),
                    "Risque réel": round(shares * risk_ps, 2)
                })
        except:
            pass

    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

# =========================
# TAB 3 — TARGETS EN R
# =========================
with tab3:
    st.header("🎯 Targets en R")

    direction_r = st.selectbox("Direction", ["Long", "Short"], key="r_dir")
    entry_r = st.number_input("Entrée", value=50.0, step=0.01, key="r_entry")
    stop_r = st.number_input("Stop", value=48.0, step=0.01, key="r_stop")

    if direction_r == "Long":
        risk_r = entry_r - stop_r
    else:
        risk_r = stop_r - entry_r

    if risk_r <= 0:
        st.error("Stop invalide.")
    else:
        targets = []

        for r in [1, 1.5, 2, 3, 4, 5]:
            if direction_r == "Long":
                target = entry_r + r * risk_r
            else:
                target = entry_r - r * risk_r

            targets.append({
                "R": f"{r}R",
                "Target": round(target, 2),
                "Gain/action": round(abs(target - entry_r), 2)
            })

        st.dataframe(pd.DataFrame(targets), use_container_width=True)

# =========================
# TAB 4 — RISQUE JOURNALIER
# =========================
with tab4:
    st.header("⚠️ Gestion du risque journalier")

    capital_day = st.number_input("Capital du compte", value=25000.0, step=500.0, key="day_cap")
    max_day_risk_pct = st.number_input("Risque journalier max (%)", value=3.0, step=0.25)
    risk_trade_pct = st.number_input("Risque par trade (%)", value=1.0, step=0.1, key="day_trade")
    losses_taken = st.number_input(
    "Pertes déjà prises aujourd'hui ($)",
    min_value=0.0,
    value=0.0,
    step=25.0
)

max_day_risk = capital_day * max_day_risk_pct / 100
risk_per_trade = capital_day * risk_trade_pct / 100
used_risk = losses_taken
remaining = max_day_risk - used_risk
    c1, c2, c3 = st.columns(3)
    c1.metric("Risque max/jour", f"${max_day_risk:,.2f}")
    c2.metric("Risque utilisé", f"${used_risk:,.2f}")
    c3.metric("Risque restant", f"${remaining:,.2f}")

    if remaining <= 0:
        st.error("Stop trading pour aujourd'hui.")
    elif remaining < risk_per_trade:
        st.warning("Tu n'as plus assez de risque pour un trade complet.")
    else:
        st.success("Tu peux encore trader selon ton plan.")

# =========================
# TAB 5 — KELLY
# =========================
with tab5:
    st.header("🧠 Kelly Criterion")

    win_rate = st.number_input("Win rate (%)", value=50.0, step=1.0)
    avg_win = st.number_input("Gain moyen ($)", value=300.0, step=25.0)
    avg_loss = st.number_input("Perte moyenne ($)", value=200.0, step=25.0)

    p = win_rate / 100
    q = 1 - p

    if avg_loss <= 0:
        st.error("Perte moyenne invalide.")
    else:
        b = avg_win / avg_loss
        kelly = p - (q / b)
        half_kelly = kelly / 2

        st.metric("Kelly optimal", f"{kelly * 100:.2f}%")
        st.metric("Demi-Kelly prudent", f"{half_kelly * 100:.2f}%")

        if kelly <= 0:
            st.error("Système non rentable selon Kelly.")
        elif kelly > 0.05:
            st.warning("Kelly est agressif. Utiliser demi-Kelly ou moins.")
        else:
            st.success("Risque raisonnable.")
