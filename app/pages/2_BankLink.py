import streamlit as st
import pandas as pd


def render_banklink_page():
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
            '<div class="bc-header-title">Link Accounts</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="bc-header-subtitle">
            Connect sandbox bank accounts or upload CSV statements so BC can build a richer,
            real-time view of your cash flows and credit capacity.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # We'll reuse this later for showing a summary
    linked_accounts_data = None
    csv_df = None

    # ================== STEP 1: CHOOSE DATA SOURCE ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="bc-pill">Step 1 · Choose Data Source</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="bc-section-caption">Use a sandbox connection for demos, or upload CSV exports from your bank / neobank.</div>',
            unsafe_allow_html=True
        )

        source_choice = st.radio(
            "How would you like to provide account and transaction data?",
            ["Sandbox demo connection", "Upload CSV file"],
            horizontal=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ================== STEP 2A: SANDBOX MODE ==================
    if source_choice == "Sandbox demo connection":
        with st.container():
            st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

            st.markdown(
                '<div class="bc-pill">Step 2 · Connect Sandbox Accounts</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="bc-section-caption">Simulate a Plaid-like flow with pre-loaded demo accounts.</div>',
                unsafe_allow_html=True
            )

            connect_clicked = st.button("🔗 Connect demo accounts")

            if connect_clicked:
                # Fake sandbox accounts
                linked_accounts_data = pd.DataFrame(
                    [
                        {
                            "Bank": "BC Demo Bank",
                            "Account name": "Student Checking",
                            "Type": "Checking",
                            "Currency": "USD",
                            "Balance": 1243.57,
                        },
                        {
                            "Bank": "BC Demo Bank",
                            "Account name": "Freelance Savings",
                            "Type": "Savings",
                            "Currency": "USD",
                            "Balance": 3120.15,
                        },
                        {
                            "Bank": "GigPay Sandbox",
                            "Account name": "Gig Wallet",
                            "Type": "Wallet",
                            "Currency": "USD",
                            "Balance": 486.90,
                        },
                    ]
                )

                st.success("✅ Demo accounts linked successfully.")
                st.dataframe(linked_accounts_data, use_container_width=True)

            else:
                st.info("Click **Connect demo accounts** to attach sample data for testing.")

            st.markdown("</div>", unsafe_allow_html=True)

    # ================== STEP 2B: CSV MODE ==================
    else:
        with st.container():
            st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

            st.markdown(
                '<div class="bc-pill">Step 2 · Upload CSV Statement</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="bc-section-caption">Upload a CSV with transactions (e.g., date, description, amount, category).</div>',
                unsafe_allow_html=True
            )

            uploaded_file = st.file_uploader(
                "Drag and drop your CSV file here, or browse files",
                type=["csv"]
            )

            if uploaded_file is not None:
                try:
                    csv_df = pd.read_csv(uploaded_file)
                    st.success("✅ CSV uploaded and parsed successfully.")
                    st.write("Preview of your data:")
                    st.dataframe(csv_df.head(20), use_container_width=True)
                except Exception as e:
                    st.error(f"Could not read the CSV file: {e}")

            else:
                st.info("No file uploaded yet. Please add a CSV file to continue.")

            st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ================== STEP 3: SUMMARY & INSIGHTS ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="bc-pill">Step 3 · Account Summary & Cash Flow</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="bc-section-caption">BC uses linked data to understand your income stability, spending patterns, and debt capacity.</div>',
            unsafe_allow_html=True
        )

        # Sandbox summary
        if source_choice == "Sandbox demo connection" and linked_accounts_data is not None:
            total_balance = linked_accounts_data["Balance"].sum()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Linked accounts", len(linked_accounts_data))
            with col2:
                st.metric("Total balance (USD)", f"${total_balance:,.2f}")
            with col3:
                avg_balance = total_balance / len(linked_accounts_data)
                st.metric("Avg. balance / account", f"${avg_balance:,.2f}")

        # CSV summary
        elif source_choice == "Upload CSV file" and csv_df is not None:
            # Try to be flexible with column names
            cols_lower = {c.lower(): c for c in csv_df.columns}

            amount_col = None
            date_col = None

            for key in ["amount", "amt", "transaction_amount"]:
                if key in cols_lower:
                    amount_col = cols_lower[key]
                    break

            for key in ["date", "transaction_date", "posted_date"]:
                if key in cols_lower:
                    date_col = cols_lower[key]
                    break

            if amount_col is not None:
                amounts = pd.to_numeric(csv_df[amount_col], errors="coerce").dropna()

                total_inflow = amounts[amounts > 0].sum()
                total_outflow = amounts[amounts < 0].sum()
                net_flow = amounts.sum()

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Transactions", len(amounts))
                with col2:
                    st.metric("Total inflows", f"${total_inflow:,.2f}")
                with col3:
                    st.metric("Total outflows", f"${total_outflow:,.2f}")

                st.metric("Net cash flow", f"${net_flow:,.2f}")

            else:
                st.info(
                    "To compute cash flow, BC expects an **Amount** column in your CSV "
                    "(e.g., 'amount', 'amt', or 'transaction_amount')."
                )
        else:
            st.info("Once you link sandbox accounts or upload a CSV, BC will show your summary here.")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------- CALL THE FUNCTION ----------
render_banklink_page()
