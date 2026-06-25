import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="TEA Trading Toolkit Pro", layout="wide")

st.title("📊 TEA Trading Toolkit Pro")

tab1, tab2, tab3, tab4 = st.tabs([
    "Position Size Pro",
    "Scénarios Stops",
    "Targets en R",
    "Risque Journalier"
])

# =========================
# TAB 1 — POSITION SIZE PRO
# =========================
with tab1:
    st.header("📌 Position Size Pro")

    col1, col2 = st.columns(2)

    with col1:
        account_size = st.number_input(
            "Capital du compte ($)",
            value=25000.0,
            step=500.0
        )

        risk_percent = st.number_input(
            "Risque par trade (%)",
            value=1.0,
            step=0.1
        )

        entry = st.number_input(
            "Prix d'entrée ($)",
            value=50.0,
            step=0.01
        )

        direction = st.selectbox(
            "Direction",
            ["Long", "Short"]
        )

    with col2:
        stop_risk_pct = st.slider(
            "Distance du stop (%)",
            min_value=0.25,
            max_value=10.0,
            value=2.0,
            step=0.25
        )

        target_r = st.slider(
            "Target en R",
            min_value=1.0,
            max_value=5.0,
            value=2.0,
            step=0.5
        )

        max_position_pct = st.slider(
            "Position maximale du compte (%)",
            min_value=10,
            max_value=200,
            value=100,
            step=10
        )

    risk_amount = account_size * risk_percent / 100

    if direction == "Long":
        stop = entry * (1 - stop_risk_pct / 100)
        risk_per_share = entry - stop
        target = entry + target_r * risk_per_share
    else:
        stop = entry * (1 + stop_risk_pct / 100)
        risk_per_share = stop - entry
        target = entry - target_r * risk_per_share

    if risk_per_share <= 0:
        st.error("Stop invalide.")
    else:
        raw_shares = math.floor(risk_amount / risk_per_share)

        max_position_value = account_size * max_position_pct / 100
        max_shares_by_position = math.floor(max_position_value / entry)

        shares = min(raw_shares, max_shares_by_position)

        position_value = shares * entry
        real_risk = shares * risk_per_share

        if direction == "Long":
            potential_gain = shares * (target - entry)
        else:
            potential_gain = shares * (entry - target)

        buying_power_used = position_value / account_size if account_size > 0 else 0

        st.divider()

        main1, main2, main3 = st.columns(3)

        main1.metric(
            "Action à prendre",
            f"{direction.upper()} {shares:,} SHARES"
        )

        main2.metric(
            "Stop calculé",
            f"${stop:.2f}"
        )

        main3.metric(
            f"Target {target_r}R",
            f"${target:.2f}"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Risque prévu", f"${risk_amount:,.2f}")
        c2.metric("Risque réel", f"${real_risk:,.2f}")
        c3.metric("Valeur position", f"${position_value:,.2f}")
        c4.metric("Buying Power", f"{buying_power_used:.2f}x")

        c5, c6, c7 = st.columns(3)

        c5.metric("Risque / action", f"${risk_per_share:.2f}")
        c6.metric("Gain potentiel", f"${potential_gain:,.2f}")
        c7.metric("Distance stop", f"{stop_risk_pct:.2f}%")

        if real_risk > risk_amount:
            st.warning("⚠️ Le risque réel dépasse le risque prévu.")

        if position_value >= max_position_value:
            st.warning("⚠️ Position limitée par le maximum de position autorisé.")

        if shares <= 0:
            st.error("Aucune position possible avec ces paramètres.")
        else:
            st.success(
                f"Plan : {direction} **{shares:,} actions** à ${entry:.2f}, "
                f"stop à ${stop:.2f}, target à ${target:.2f}."
            )

# =========================
# TAB 2 — SCÉNARIOS STOPS
# =========================
with tab2:
    st.header("📉 Scénarios de stops")

    col1, col2 = st.columns(2)

    with col1:
        account = st.number_input(
            "Capital ($)",
            value=25000.0,
            step=500.0,
            key="sc_account"
        )

        risk_pct = st.number_input(
            "Risque (%)",
            value=1.0,
            step=0.1,
            key="sc_risk"
        )

        entry_sc = st.number_input(
            "Entrée",
            value=50.0,
            step=0.01,
            key="sc_entry"
        )

        direction_sc = st.selectbox(
            "Direction",
            ["Long", "Short"],
            key="sc_direction"
        )

    with col2:
        stop_pct_text = st.text_area(
            "Distances de stop en %, une par ligne",
            "0.5\n1\n1.5\n2\n3\n5"
        )

    risk_dollars = account * risk_pct / 100
    rows = []

    for s in stop_pct_text.splitlines():
        try:
            stop_pct = float(s.strip())
            if stop_pct <= 0:
                continue

            if direction_sc == "Long":
                stop_val = entry_sc * (1 - stop_pct / 100)
                risk_ps = entry_sc - stop_val
            else:
                stop_val = entry_sc * (1 + stop_pct / 100)
                risk_ps = stop_val - entry_sc

            shares = math.floor(risk_dollars / risk_ps)

            rows.append({
                "Stop %": stop_pct,
                "Stop": round(stop_val, 2),
                "Risque/action": round(risk_ps, 2),
                "Actions": shares,
                "Valeur position": round(shares * entry_sc, 2),
                "Risque réel": round(shares * risk_ps, 2),
            })

        except Exception:
            pass

    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

# =========================
# TAB 3 — TARGETS EN R
# =========================
with tab3:
    st.header("🎯 Targets en R")

    col1, col2 = st.columns(2)

    with col1:
        direction_r = st.selectbox("Direction", ["Long", "Short"], key="r_dir")
        entry_r = st.number_input("Entrée", value=50.0, step=0.01, key="r_entry")
        stop_pct_r = st.number_input("Distance stop (%)", value=2.0, step=0.1, key="r_stop_pct")

    with col2:
        if direction_r == "Long":
            stop_r = entry_r * (1 - stop_pct_r / 100)
            risk_r = entry_r - stop_r
        else:
            stop_r = entry_r * (1 + stop_pct_r / 100)
            risk_r = stop_r - entry_r

        st.metric("Stop calculé", f"${stop_r:.2f}")

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

    col1, col2 = st.columns(2)

    with col1:
        capital_day = st.number_input(
            "Capital du compte",
            value=25000.0,
            step=500.0,
            key="day_cap"
        )

        max_day_risk_pct = st.number_input(
            "Risque journalier max (%)",
            value=3.0,
            step=0.25
        )

        risk_trade_pct = st.number_input(
            "Risque par trade (%)",
            value=1.0,
            step=0.1,
            key="day_trade"
        )

    with col2:
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

    trades_left = math.floor(remaining / risk_per_trade) if risk_per_trade > 0 else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Risque max/jour", f"${max_day_risk:,.2f}")
    c2.metric("Risque utilisé", f"${used_risk:,.2f}")
    c3.metric("Risque restant", f"${remaining:,.2f}")
    c4.metric("Trades complets restants", f"{trades_left}")

    if remaining <= 0:
        st.error("🛑 Stop trading pour aujourd'hui.")
    elif remaining < risk_per_trade:
        st.warning("⚠️ Tu n'as plus assez de risque pour un trade complet.")
    else:
        st.success("✅ Tu peux encore trader selon ton plan.")
