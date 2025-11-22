import streamlit as st
import pandas as pd
import numpy as np


def render_ai_credit_dashboard_page():
    # ---------- LIGHT CUSTOM STYLING ----------
    st.markdown(
        """
        <style>
        .main {
            padding-top: 0.5rem;
            padding-bottom: 2rem;
        }

        .bc-header-title {
            font-size: 1.9rem;
            font-weight: 700;
            margin-top: 0rem;
            margin-bottom: 0.1rem;
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

        .bc-section-caption {
            font-size: 0.85rem;
            color: #A0AEC0;
            margin-bottom: 0.75rem;
        }

        .bc-card-box {
            background: #0b1220;
            border-radius: 14px;
            padding: 1rem 1rem;
            border: 1px solid #1f2937;
            margin-bottom: 0.7rem;
        }

        .bc-badge {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .bc-badge-low {
            background: #065f46;
            color: #d1fae5;
        }
        .bc-badge-medium {
            background: #92400e;
            color: #ffedd5;
        }
        .bc-badge-high {
            background: #7f1d1d;
            color: #fee2e2;
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
        st.markdown(
            '<div class="bc-header-title">AI Credit Dashboard</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="bc-header-subtitle">
            See how BC’s AI interprets your linked accounts, income signals, and risk profile
            to generate a portable, borderless credit limit.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ================== PROFILE SNAPSHOT ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown(
            '<div class="bc-pill">Profile Snapshot</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="bc-section-caption">High-level status of your onboarding and data quality.</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            kyc_status = st.selectbox(
                "KYC status (for demo)",
                ["Not started", "In review", "Verified"],
                index=2
            )

        with col2:
            accounts_linked = st.number_input(
                "Accounts linked",
                min_value=0,
                max_value=10,
                value=3
            )

        with col3:
            countries_seen = st.number_input(
                "Countries of income",
                min_value=1,
                max_value=10,
                value=2
            )

        with col4:
            months_history = st.number_input(
                "Months of transaction history",
                min_value=0,
                max_value=60,
                value=12
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ================== AI INPUTS & SCORE ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown(
            '<div class="bc-pill">AI Inputs & Score</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="bc-section-caption">Adjust the sliders to see how behavior affects your BC AI credit score and limit.</div>',
            unsafe_allow_html=True
        )

        left, right = st.columns([1.2, 1])

        with left:
            profile_type = st.selectbox(
                "Profile type",
                ["International student", "Freelancer / gig worker", "New immigrant", "Remote employee"],
                index=0
            )

            monthly_income = st.slider(
                "Stable monthly income (USD equivalent)",
                min_value=200,
                max_value=8000,
                value=1800,
                step=100
            )

            income_volatility = st.slider(
                "Income volatility (0 = very stable, 100 = very volatile)",
                min_value=0,
                max_value=100,
                value=35
            )

            utilization = st.slider(
                "Credit / wallet utilization (%)",
                min_value=0,
                max_value=100,
                value=42
            )

            missed_payments = st.slider(
                "Missed / late payments in last 12 months",
                min_value=0,
                max_value=10,
                value=0
            )

            country_risk = st.selectbox(
                "Jurisdiction risk (where most of your income flows come from)",
                ["Low", "Medium", "High"],
                index=1
            )

        # ----- SIMPLE "AI" SCORING LOGIC (for demo only) -----
        base_score = 650

        # Income effect
        if monthly_income < 800:
            base_score -= 80
        elif monthly_income < 1500:
            base_score -= 40
        elif monthly_income > 3500:
            base_score += 30
        elif monthly_income > 5000:
            base_score += 50

        # Volatility (higher volatility = lower score)
        base_score -= (income_volatility * 0.6)

        # Utilization (sweet spot around 20–40%)
        if utilization < 10:
            base_score -= 10
        elif 10 <= utilization <= 40:
            base_score += 20
        elif utilization > 80:
            base_score -= 40

        # Missed payments
        base_score -= missed_payments * 25

        # Country risk
        if country_risk == "Low":
            base_score += 20
        elif country_risk == "High":
            base_score -= 30

        # Data depth (months of history + accounts)
        base_score += min(months_history, 24) * 0.8
        base_score += min(accounts_linked, 5) * 4

        # KYC bonus
        if kyc_status == "Verified":
            base_score += 20
        elif kyc_status == "In review":
            base_score += 5

        # Clamp
        ai_score = int(np.clip(base_score, 300, 900))

        # Risk bucket
        if ai_score >= 760:
            risk_level = "Low"
            badge_class = "bc-badge-low"
        elif ai_score >= 620:
            risk_level = "Medium"
            badge_class = "bc-badge-medium"
        else:
            risk_level = "High"
            badge_class = "bc-badge-high"

        # Recommended limit (simple function of income and score)
        limit_base = monthly_income * 1.5
        limit_multiplier = (ai_score - 300) / 600  # 0–1 range
        recommended_limit = int(limit_base * limit_multiplier)

        with right:
            st.markdown("#### AI Credit Summary")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("BC AI Score", f"{ai_score} / 900")
            with col_b:
                st.metric("Suggested BC Limit", f"${recommended_limit:,.0f}")

            st.markdown(
                f'<span class="bc-badge {badge_class}">Risk level: {risk_level}</span>',
                unsafe_allow_html=True
            )

            st.write("")
            st.caption(
                "This score is generated by BC’s experimental scoring engine using income stability, "
                "volatility, utilization, repayment behavior, and jurisdiction risk. "
                "In production, this would be backed by real ML models and linked accounts."
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ================== SCENARIO SANDBOX ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown(
            '<div class="bc-pill">Scenario Sandbox</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="bc-section-caption">Compare your current behavior with a “healthier” scenario and see how your limit could change.</div>',
            unsafe_allow_html=True
        )

        col_now, col_target = st.columns(2)

        with col_now:
            st.subheader("Current pattern")
            st.write(f"• Utilization: **{utilization}%**")
            st.write(f"• Income volatility: **{income_volatility}/100**")
            st.write(f"• Missed payments: **{missed_payments}**")
            st.write(f"• Risk level: **{risk_level}**")
            st.write(f"• Suggested limit: **${recommended_limit:,.0f}**")

        with col_target:
            st.subheader("Improved pattern (what-if)")

            improved_util = st.slider(
                "Target utilization (%)",
                min_value=0,
                max_value=100,
                value=max(5, min(utilization, 35)),
                key="improved_util"
            )
            improved_vol = st.slider(
                "Target volatility (0–100)",
                min_value=0,
                max_value=100,
                value=max(0, min(income_volatility, 25)),
                key="improved_vol"
            )
            improved_missed = st.slider(
                "Target missed payments (next 12 months)",
                min_value=0,
                max_value=10,
                value=0,
                key="improved_missed"
            )

            # Re-score quickly with improved behavior
            improved_score = base_score  # start from same base before some penalties
            # Remove old penalties: approximate adjustment
            improved_score += (income_volatility - improved_vol) * 0.6
            if improved_util <= 40 and utilization > 40:
                improved_score += 25
            improved_score += (missed_payments - improved_missed) * 25

            improved_score = int(np.clip(improved_score, 300, 900))
            improved_limit = int(limit_base * ((improved_score - 300) / 600))

            st.write(f"**AI Score (what-if):** {improved_score} / 900")
            st.write(f"**Suggested limit (what-if):** ${improved_limit:,.0f}")

            delta_score = improved_score - ai_score
            delta_limit = improved_limit - recommended_limit

            if delta_score > 0:
                st.success(f"Score improvement: +{delta_score} points")
            elif delta_score < 0:
                st.warning(f"Score decrease: {delta_score} points")
            else:
                st.info("No change in score.")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------- CALL THE FUNCTION ----------
render_ai_credit_dashboard_page()
