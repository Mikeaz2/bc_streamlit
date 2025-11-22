import streamlit as st

def render_kyc_page():
    # ---------- OPTIONAL: PAGE CONFIG (only if this is a standalone page) ----------
    st.set_page_config(
        page_title="BC – KYC & Onboarding",
        page_icon="app/assets/bc-logo.png",
        layout="wide"
    )

    # ---------- LIGHT CUSTOM STYLING (reuse from home, plus a bit extra) ----------
    st.markdown(
        """
        <style>
        .main {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .bc-header-title {
            font-size: 1.9rem;
            font-weight: 700;
            margin-bottom: 0.15rem;
        }

        .bc-header-subtitle {
            font-size: 1.05rem;
            color: #A0AEC0;
            margin-bottom: 0.4rem;
        }

        .bc-section-title {
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .bc-section-caption {
            font-size: 0.85rem;
            color: #A0AEC0;
            margin-bottom: 0.75rem;
        }

        .bc-card-box {
            background: #0b1220;
            border-radius: 14px;
            padding: 1rem 1.1rem;
            border: 1px solid #1f2937;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------- HEADER ----------
    col_logo, col_text = st.columns([1, 2.2])

    with col_logo:
        st.image("app/assets/bc-logo.png", width=250)

    with col_text:
        st.markdown(
            '<div class="bc-header-title">KYC & Onboarding</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="bc-header-subtitle">
            Verify your identity once and unlock borderless credit limits you can carry
            across countries, gigs, and studies.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ---------- KYC FORM ----------
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="bc-section-title">Step 1 · Basic Identity</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="bc-section-caption">We only ask for what is required by global KYC / AML standards.</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full legal name (as on ID)")
            dob = st.date_input("Date of birth")
            nationality = st.text_input("Nationality")
        with col2:
            residency_country = st.text_input("Country of current residence")
            phone = st.text_input("Mobile number (with country code)")
            email = st.text_input("Email address")

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")  # small vertical space

    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="bc-section-title">Step 2 · Government ID</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="bc-section-caption">Upload one valid photo ID and a selfie. We use this only for verification.</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            id_type = st.selectbox(
                "ID type",
                ["Passport", "National ID card", "Driver’s license", "Residence permit"]
            )
            id_number = st.text_input("ID number")
            id_issue_country = st.text_input("ID issuing country")
        with col2:
            id_doc = st.file_uploader(
                "Upload ID document (front / main page)",
                type=["jpg", "jpeg", "png", "pdf"]
            )
            selfie = st.file_uploader(
                "Upload live selfie",
                type=["jpg", "jpeg", "png"]
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="bc-section-title">Step 3 · Address & Financial Profile</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="bc-section-caption">This helps us assess your risk profile and offer fair credit limits.</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            address_line = st.text_input("Street address")
            city = st.text_input("City")
            postal_code = st.text_input("Postal / ZIP code")
        with col2:
            employment_status = st.selectbox(
                "Employment status",
                [
                    "Student",
                    "Employed full-time",
                    "Employed part-time / gig worker",
                    "Self-employed / freelancer",
                    "Unemployed",
                    "Other"
                ]
            )
            income_range = st.selectbox(
                "Approximate monthly income (equivalent in USD)",
                [
                    "Below $500",
                    "$500 – $1,000",
                    "$1,000 – $2,000",
                    "$2,000 – $3,500",
                    "$3,500 – $5,000",
                    "Above $5,000"
                ]
            )
            source_of_funds = st.multiselect(
                "Main source(s) of funds",
                [
                    "Salary",
                    "Freelance / gig income",
                    "Scholarship / stipend",
                    "Family support",
                    "Business income",
                    "Savings / investments"
                ]
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ---------- CONSENT & SUBMIT ----------
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="bc-section-title">Final Step · Consent & Submit</div>',
            unsafe_allow_html=True
        )

        agree_terms = st.checkbox(
            "I confirm that the information provided is accurate and I agree to BC’s terms, "
            "privacy policy, and KYC / AML checks."
        )

        submitted = st.button("Submit for verification")

        if submitted:
            if not agree_terms:
                st.error("Please confirm that the information is accurate and accept the terms to continue.")
            elif not full_name or not email or not id_doc or not selfie:
                st.warning(
                    "Please make sure you filled your name, email, uploaded your ID document and selfie."
                )
            else:
                # Here you would save to your backend / database
                st.success("✅ KYC submitted. Your profile is now under review. We’ll notify you once it’s verified.")

        st.markdown("</div>", unsafe_allow_html=True)
