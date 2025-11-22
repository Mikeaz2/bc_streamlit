import streamlit as st
import pandas as pd
import numpy as np
from components.bc_assistant import render_bc_assistant   # ✅ ADDED


def init_borrowers_state():
    """Initialize borrowers in session_state if not already set."""
    if "borrowers" not in st.session_state:
        borrowers = pd.DataFrame(
            [
                {
                    "ID": 1,
                    "Name": "John Rivera",
                    "Country": "Philippines",
                    "Requested": 150,
                    "AI Score": 712,
                    "Volatility": 27,
                    "Flags": "Low volatility, Clean history",
                    "Status": "In review",
                    "Wallet balance": 45,
                    "Bank balance": 320,
                },
                {
                    "ID": 2,
                    "Name": "Lina Chen",
                    "Country": "Malaysia",
                    "Requested": 80,
                    "AI Score": 640,
                    "Volatility": 48,
                    "Flags": "Medium volatility",
                    "Status": "In review",
                    "Wallet balance": 120,
                    "Bank balance": 510,
                },
                {
                    "ID": 3,
                    "Name": "Samuel Okoro",
                    "Country": "Kenya",
                    "Requested": 220,
                    "AI Score": 560,
                    "Volatility": 72,
                    "Flags": "High volatility, Thin file",
                    "Status": "In review",
                    "Wallet balance": 30,
                    "Bank balance": 190,
                },
                {
                    "ID": 4,
                    "Name": "Maria Gomez",
                    "Country": "Colombia",
                    "Requested": 300,
                    "AI Score": 785,
                    "Volatility": 18,
                    "Flags": "Strong stability",
                    "Status": "Approved",
                    "Wallet balance": 260,
                    "Bank balance": 1100,
                },
            ]
        )

        # Derive a simple risk band from AI score
        def risk_band(score):
            if score >= 760:
                return "Low"
            elif score >= 620:
                return "Medium"
            else:
                return "High"

        borrowers["Risk band"] = borrowers["AI Score"].apply(risk_band)
        st.session_state["borrowers"] = borrowers


def get_transaction_history(name: str) -> pd.DataFrame:
    """Return a simple demo transaction history per borrower."""
    # In a real system this would query a database.
    # Here we just hard-code / generate some fake but realistic rows.
    base_data = {
        "John Rivera": [
            ("2025-10-01", "Gig payout", 85.0, "Wallet"),
            ("2025-10-05", "Transfer to bank", -60.0, "Wallet → Bank"),
            ("2025-10-12", "Food & groceries", -30.5, "Card"),
            ("2025-10-20", "Micro-loan repayment", -12.0, "Wallet"),
        ],
        "Lina Chen": [
            ("2025-09-28", "Part-time salary", 220.0, "Bank"),
            ("2025-10-03", "Rent", -150.0, "Bank"),
            ("2025-10-10", "Online purchase", -20.0, "Card"),
            ("2025-10-19", "Study stipend", 120.0, "Bank"),
        ],
        "Samuel Okoro": [
            ("2025-09-30", "Ride-hailing income", 40.0, "Wallet"),
            ("2025-10-04", "Fuel", -18.0, "Wallet"),
            ("2025-10-11", "Top-up from bank", 25.0, "Bank → Wallet"),
            ("2025-10-17", "Loan repayment", -10.0, "Wallet"),
        ],
        "Maria Gomez": [
            ("2025-09-25", "Remote salary", 600.0, "Bank"),
            ("2025-09-30", "Savings transfer", -200.0, "Bank"),
            ("2025-10-07", "Flight ticket", -150.0, "Card"),
            ("2025-10-15", "Bonus payout", 150.0, "Bank"),
        ],
    }

    rows = base_data.get(
        name,
        [
            ("2025-10-01", "Balance forward", 0.0, "System"),
        ],
    )
    return pd.DataFrame(rows, columns=["Date", "Description", "Amount (USD)", "Channel"])


def render_lender_portal():

    init_borrowers_state()
    borrowers = st.session_state["borrowers"]

    # ---------- PAGE STYLE ----------
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
            margin-bottom: 1rem;
        }

        .bc-pill {
            display: inline-block;
            background: #111827;
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-weight: 600;
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

        .approved { color: #10b981; font-weight:600; }
        .denied { color: #ef4444; font-weight:600; }
        .review { color: #fbbf24; font-weight:600; }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------- HEADER ----------
    col_logo, col_text = st.columns([1, 2.2])

    with col_logo:
        st.image("app/assets/bc-logo.png", width=250)

    with col_text:
        st.markdown('<div class="bc-header-title">Lender Portal</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="bc-header-subtitle">
            Review borrower applications, evaluate AI scores & risk flags, simulate disbursements,
            and export your pipeline.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ================== PORTFOLIO OVERVIEW ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="bc-pill">Portfolio Overview</div>', unsafe_allow_html=True)

        colA, colB, colC, colD = st.columns(4)

        with colA:
            st.metric("Total applications", len(borrowers))

        with colB:
            st.metric("Approved", borrowers[borrowers["Status"] == "Approved"].shape[0])

        with colC:
            st.metric("In review", borrowers[borrowers["Status"] == "In review"].shape[0])

        with colD:
            avg_score = int(borrowers["AI Score"].mean())
            st.metric("Avg. AI score", avg_score)

        st.markdown("</div>", unsafe_allow_html=True)

    # ================== FILTERS & DOWNLOAD ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="bc-pill">Filters & Export</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            country_filter = st.multiselect(
                "Country",
                sorted(borrowers["Country"].unique().tolist()),
                default=sorted(borrowers["Country"].unique().tolist()),
            )

        with col2:
            risk_filter = st.multiselect(
                "Risk band",
                ["Low", "Medium", "High"],
                default=["Low", "Medium", "High"],
            )

        with col3:
            score_min, score_max = st.slider(
                "AI score range",
                min_value=int(borrowers["AI Score"].min()),
                max_value=int(borrowers["AI Score"].max()),
                value=(
                    int(borrowers["AI Score"].min()),
                    int(borrowers["AI Score"].max()),
                ),
            )

        vol_max = st.slider(
            "Max volatility (0–100)",
            min_value=0,
            max_value=100,
            value=100,
        )

        # Apply filters
        filt = (
            borrowers["Country"].isin(country_filter)
            & borrowers["Risk band"].isin(risk_filter)
            & borrowers["AI Score"].between(score_min, score_max)
            & (borrowers["Volatility"] <= vol_max)
        )
        filtered = borrowers[filt].copy()

        st.write("Filtered applications:")
        st.dataframe(
            filtered[["Name", "Country", "Risk band", "Requested", "AI Score", "Volatility", "Status"]],
            use_container_width=True,
        )

        st.write("")
        csv_data = borrowers.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download borrower data (CSV)",
            data=csv_data,
            file_name="bc_borrowers_demo.csv",
            mime="text/csv",
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ================== REAL-TIME APPROVAL QUEUE ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="bc-pill">Real-Time Approval Queue</div>', unsafe_allow_html=True)

        queue = borrowers[borrowers["Status"] == "In review"][["Name", "Country", "Requested", "AI Score", "Risk band"]]

        if queue.empty:
            st.info("No applications in review. All caught up ✅")
        else:
            st.dataframe(queue, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ================== BORROWER SELECTION ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="bc-pill">Borrower Detail</div>', unsafe_allow_html=True)

        if filtered.empty:
            st.warning("No borrowers match the current filters. Adjust filters to view applicants.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        selected_name = st.selectbox(
            "Choose an applicant to review",
            filtered["Name"].tolist(),
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # Get the selected borrower (from the full table, not just filtered)
    borrowers = st.session_state["borrowers"]  # re-read in case updated
    borrower_row = borrowers[borrowers["Name"] == selected_name].iloc[0]
    idx = borrowers[borrowers["Name"] == selected_name].index[0]

    # ================== BORROWER DETAILS PANEL ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="bc-pill">Applicant: {borrower_row["Name"]}</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(f"**Country:** {borrower_row['Country']}")
            st.write(f"**Risk band:** {borrower_row['Risk band']}")
            st.write(f"**Status:** {borrower_row['Status']}")

        with col2:
            st.write(f"**Requested amount:** ${borrower_row['Requested']}")
            st.write(f"**AI Score:** {borrower_row['AI Score']}")
            st.write(f"**Volatility:** {borrower_row['Volatility']}/100")

        with col3:
            st.write(f"**Wallet balance:** ${borrower_row['Wallet balance']}")
            st.write(f"**Bank balance:** ${borrower_row['Bank balance']}")
            st.write(f"**Flags:** {borrower_row['Flags']}")

        # Risk flags chips
        st.write("### Risk Flags")
        flags_list = [f.strip() for f in borrower_row["Flags"].split(",")]
        for f in flags_list:
            st.markdown(f'<span class="bc-flag-chip">{f}</span>', unsafe_allow_html=True)

        # -------- Borrower profile "modal" (expander) --------
        with st.expander("View full borrower profile"):
            st.write("**Segment:** International student / cross-border worker (demo)")
            st.write("**Primary income sources:** Remote work / gig income (demo)")
            st.write("**Credit notes (BC internal):**")
            st.write(
                "- Early adopter of BC\n"
                "- Engages regularly with the app\n"
                "- No severe delinquencies in the past 12 months (demo)"
            )

        # ---------- AI Recommendation ----------
        score = borrower_row["AI Score"]
        vol = borrower_row["Volatility"]

        if score >= 760 and vol < 40:
            recommendation = "Strong approve"
            rationale = "High score + low volatility = safe for micro-loan."
        elif score >= 630 and vol < 60:
            recommendation = "Approve with standard limit"
            rationale = "Decent score but moderate volatility = manageable risk."
        elif score >= 580:
            recommendation = "Review manually / consider lower limit"
            rationale = "Middle score + high volatility = borderline case."
        else:
            recommendation = "Decline"
            rationale = "Low score + high volatility = too risky for micro-loan."

        st.write("")
        st.markdown("### BC AI Recommendation")
        st.write(f"**Recommendation:** {recommendation}")
        st.caption(rationale)

        # ================== TRANSACTION HISTORY ==================
        st.write("")
        st.markdown("### Recent Transaction History (for context)")
        tx_df = get_transaction_history(borrower_row["Name"])
        st.dataframe(tx_df, use_container_width=True)

        # ================== LOAN DISBURSEMENT SIMULATION ==================
        st.write("")
        st.markdown("### Disbursement Simulation")

        disburse_channel = st.radio(
            "Disburse to",
            ["BC Wallet", "Local bank account"],
            horizontal=True,
        )

        # Suggested max exposure given risk band
        if borrower_row["Risk band"] == "Low":
            exposure_factor = 1.0
        elif borrower_row["Risk band"] == "Medium":
            exposure_factor = 0.7
        else:
            exposure_factor = 0.4

        suggested_limit = int(borrower_row["Requested"] * exposure_factor)

        st.write(f"**Requested:** ${borrower_row['Requested']} · **Suggested maximum exposure:** ${suggested_limit}")

        disburse_amount = st.slider(
            "Disbursement amount (for this decision)",
            min_value=0,
            max_value=int(borrower_row["Requested"]),
            value=min(suggested_limit, int(borrower_row["Requested"])),
            step=10,
        )

        # ================== APPROVE / DECLINE BUTTONS ==================
        st.write("")
        st.markdown("### Lender Decision")

        colA, colB = st.columns(2)

        with colA:
            approve_clicked = st.button("✅ Approve and simulate disbursement")
        with colB:
            decline_clicked = st.button("❌ Decline this application")

        # Handle decisions with state updates
        if approve_clicked and disburse_amount > 0:
            borrowers = st.session_state["borrowers"]
            borrowers.at[idx, "Status"] = "Approved"

            # Simulate funds movement
            if disburse_channel == "BC Wallet":
                borrowers.at[idx, "Wallet balance"] = borrowers.at[idx, "Wallet balance"] + disburse_amount
            else:
                borrowers.at[idx, "Bank balance"] = borrowers.at[idx, "Bank balance"] + disburse_amount

            st.session_state["borrowers"] = borrowers

            st.success(
                f"Approved ${disburse_amount} to {disburse_channel} for {borrower_row['Name']} (demo simulation only)."
            )
            st.caption("In production, this would trigger a real disbursement via a payments rail / partner.")
        elif approve_clicked and disburse_amount == 0:
            st.warning("Disbursement amount must be greater than 0 to approve.")

        if decline_clicked:
            borrowers = st.session_state["borrowers"]
            borrowers.at[idx, "Status"] = "Declined"
            st.session_state["borrowers"] = borrowers
            st.error(f"Application for {borrower_row['Name']} marked as Declined.")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------- CALL ----------
render_lender_portal()

# ---------- FLOATING BC ASSISTANT ----------
render_bc_assistant()   # ✅ ADDED
