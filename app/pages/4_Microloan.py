import streamlit as st
import numpy as np
import pandas as pd
from components.bc_assistant import render_bc_assistant   # ✅ ADDED


def render_microloan_page():

    # ---------- SESSION STATE FOR ACCEPTANCE ----------
    if "loan_accepted" not in st.session_state:
        st.session_state["loan_accepted"] = False

    # ---------- STYLE ----------
    st.markdown(
        """
        <style>
        .bc-header-title {
            font-size: 1.9rem;
            font-weight: 700;
            margin-top: 0rem;
            margin-bottom: 0.2rem;
        }

        .bc-header-subtitle {
            font-size: 1.05rem;
            color: #A0AEC0;
            margin-top: 0rem;
            margin-bottom: 1rem;
        }

        .bc-pill {
            display: inline-block;
            background: #111827;
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.92rem;
            border: 1px solid #1f2937;
            margin-bottom: 0.4rem;
        }

        .bc-card-box {
            background: #0b1220;
            border-radius: 16px;
            padding: 1.2rem;
            border: 1px solid #1f2937;
            margin-bottom: 0.8rem;
        }

        .bc-offer-box {
            background: #0d1729;
            border-radius: 16px;
            padding: 1.3rem;
            border: 1px solid #1e293b;
            box-shadow: 0 0 20px rgba(0,0,0,0.35);
            margin-bottom: 0.9rem;
        }

        .bc-badge-approved {
            background: #065f46;
            color: #d1fae5;
            padding: 0.25rem 0.65rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .bc-badge-manual {
            background: #92400e;
            color: #ffedd5;
            padding: 0.25rem 0.65rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .bc-badge-denied {
            background: #7f1d1d;
            color: #fee2e2;
            padding: 0.25rem 0.65rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .bc-flag-chip {
            display: inline-block;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            font-size: 0.78rem;
            margin-right: 0.3rem;
            margin-bottom: 0.3rem;
            border: 1px solid #374151;
            background: #020617;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------- HEADER ----------
    col_logo, col_text = st.columns([1, 2])

    with col_logo:
        st.image("app/assets/bc-logo.png", width=250)

    with col_text:
        st.markdown('<div class="bc-header-title">Instant Micro-Loan Offer</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="bc-header-subtitle">
            BC’s AI analyzes your cash-flow stability, spending patterns, and credit signals
            to generate real-time micro-loan offers you can use instantly.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ================== STEP 1: USER INPUTS ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown('<div class="bc-pill">Loan Preferences</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            request_amount = st.slider(
                "Loan amount requested",
                min_value=20,
                max_value=800,
                value=120,
                step=10
            )

            duration_weeks = st.slider(
                "Repayment duration (weeks)",
                min_value=2,
                max_value=24,
                value=8
            )

        with col2:
            repayment_frequency = st.selectbox(
                "Repayment frequency",
                ["Weekly", "Bi-Weekly", "Monthly"]
            )

            purpose = st.selectbox(
                "Loan purpose",
                ["Education", "Living expenses", "Travel", "Emergencies", "Other"]
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ================== STEP 2: BC AI SCORE (FAKE DEMO) ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="bc-pill">AI Score Inputs (Demo)</div>', unsafe_allow_html=True)

        col3, col4 = st.columns(2)

        with col3:
            ai_score = st.slider("BC AI Score (demo)", min_value=300, max_value=900, value=720)
        with col4:
            volatility = st.slider("Cash-flow volatility (0–100)", min_value=0, max_value=100, value=30)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ================== STEP 3: AI LOAN DECISION ==================
    approval_score_cutoff = 630
    auto_approval_cutoff = 720

    # Risk penalty based on volatility
    volatility_penalty = volatility * 0.4

    # Final score used for decision
    final_score = ai_score - volatility_penalty

    if final_score >= auto_approval_cutoff:
        decision = "Approved"
        badge_class = "bc-badge-approved"
    elif final_score >= approval_score_cutoff:
        decision = "Needs manual review"
        badge_class = "bc-badge-manual"
    else:
        decision = "Declined"
        badge_class = "bc-badge-denied"

    # APR calculation (simple risk-adjusted)
    base_apr = 9.5
    risk_adj = (700 - ai_score) / 20
    volatility_adj = volatility / 15
    apr = max(5.9, base_apr + risk_adj + volatility_adj)

    # Max amount offered
    max_offer = int((final_score - 300) / 600 * 600)
    max_offer = int(np.clip(max_offer, 30, 600))

    # Align offer with user request
    approved_amount = max(0, min(request_amount, max_offer))

    # ---------- INTEREST + REPAYMENT CALC ----------
    if approved_amount > 0 and decision != "Declined":
        term_years = duration_weeks / 52
        simple_interest = approved_amount * (apr / 100) * term_years
        total_repay = approved_amount + simple_interest
    else:
        term_years = 0
        simple_interest = 0
        total_repay = 0

    # Number of payments based on frequency
    if repayment_frequency == "Weekly":
        num_payments = duration_weeks
        period_label = "Week"
    elif repayment_frequency == "Bi-Weekly":
        num_payments = max(1, duration_weeks // 2)
        period_label = "Bi-week"
    else:  # Monthly
        num_payments = max(1, round(duration_weeks / 4))
        period_label = "Month"

    num_payments = int(max(1, num_payments))

    if approved_amount > 0 and decision != "Declined":
        payment_per = total_repay / num_payments
        principal_per = approved_amount / num_payments
        interest_per = simple_interest / num_payments
    else:
        payment_per = principal_per = interest_per = 0

    # Build repayment schedule
    schedule_rows = []
    remaining = approved_amount

    for i in range(1, num_payments + 1):
        if remaining <= 0:
            principal_i = 0
        else:
            principal_i = min(principal_per, remaining)
        interest_i = interest_per
        total_i = principal_i + interest_i
        remaining = max(0, remaining - principal_i)

        schedule_rows.append(
            {
                "#": i,
                "Period": f"{period_label} {i}",
                "Principal": round(principal_i, 2),
                "Interest": round(interest_i, 2),
                "Total payment": round(total_i, 2),
                "Remaining balance": round(remaining, 2),
            }
        )

    schedule_df = pd.DataFrame(schedule_rows)

    # ================== OFFER CARD ==================
    with st.container():
        st.markdown('<div class="bc-offer-box">', unsafe_allow_html=True)

        st.markdown(
            f'<span class="{badge_class}">{decision}</span>',
            unsafe_allow_html=True
        )

        st.markdown("### Your BC Micro-Loan Offer")

        if approved_amount <= 0 or decision == "Declined":
            st.write("Based on your current AI score and volatility, BC cannot extend this micro-loan automatically.")
        else:
            colA, colB, colC = st.columns(3)
            with colA:
                st.metric("Approved amount", f"${approved_amount}")
            with colB:
                st.metric("APR", f"{apr:.2f}%")
            with colC:
                st.metric("Duration", f"{duration_weeks} weeks")

            st.write(f"**Estimated {repayment_frequency.lower()} payment:** ${payment_per:,.2f}")

        st.caption(
            "Offer is generated by BC’s real-time scoring system using income signals, "
            "volatility, repayment behavior, and multi-country cash-flow patterns."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ================== STEP 4: INTEREST BREAKDOWN + SCHEDULE ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="bc-pill">Interest & Repayment Schedule</div>', unsafe_allow_html=True)

        if approved_amount <= 0 or decision == "Declined":
            st.info("No repayment schedule is generated because this offer is not approved.")
        else:
            colX, colY, colZ = st.columns(3)
            with colX:
                st.metric("Principal", f"${approved_amount:,.2f}")
            with colY:
                st.metric("Interest cost over term", f"${simple_interest:,.2f}")
            with colZ:
                st.metric("Total to repay", f"${total_repay:,.2f}")

            st.write("**Repayment schedule**")
            st.dataframe(schedule_df, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ================== STEP 5: FLAGS ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="bc-pill">Flags</div>', unsafe_allow_html=True)

        flags = []
        if volatility > 60:
            flags.append("High volatility risk")
        if ai_score < 600:
            flags.append("Weak AI score")
        if request_amount > max_offer:
            flags.append("Requested amount above safe threshold")
        if decision == "Needs manual review":
            flags.append("Requires human verification")
        if decision == "Approved":
            flags.append("Profile stable enough for instant approval")

        if flags:
            for f in flags:
                st.markdown(
                    f'<span class="bc-flag-chip">{f}</span>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<span class="bc-flag-chip">No major risk flags detected</span>',
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ================== STEP 6: ONE-TAP ACCEPT ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="bc-pill">Confirm Micro-Loan</div>', unsafe_allow_html=True)

        if decision == "Declined" or approved_amount <= 0:
            st.warning("This loan cannot be accepted because it was not approved by BC’s AI.")
        else:
            accept_clicked = st.button("✅ Accept this loan")

            if accept_clicked:
                st.session_state["loan_accepted"] = True

            if st.session_state["loan_accepted"]:
                st.success("✅ Loan accepted successfully.")
                st.write(
                    f"You’ve accepted a micro-loan of **${approved_amount:,.2f}** "
                    f"at **{apr:.2f}% APR** over **{duration_weeks} weeks**."
                )
                st.write(
                    f"Your estimated {repayment_frequency.lower()} payment is **${payment_per:,.2f}**, "
                    f"for a total repayment of **${total_repay:,.2f}**."
                )
                st.caption("In a real deployment, funds would now be disbursed to your chosen wallet or bank account.")
                st.balloons()
            else:
                st.info("Review your offer and repayment schedule above, then tap **Accept this loan** to confirm.")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------- CALL ----------
render_microloan_page()

# ---------- FLOATING BC ASSISTANT ----------
render_bc_assistant()   # ✅ ADDED
