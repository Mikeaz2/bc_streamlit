import streamlit as st


def render_kyc_page():
    # ---------- LIGHT CUSTOM STYLING ----------
    st.markdown(
        """
        <style>
        .main {
            padding-top: 0.5rem;     /* reduced spacing */
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
            margin-bottom: 1rem;    /* space below subtitle */
        }

        /* PILL STYLE TITLES */
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

    # ---------- PROGRESS BAR PLACEHOLDER ----------
    progress_placeholder = st.empty()

    # ================== STEP 1: BASIC IDENTITY ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="bc-pill">Step 1 · Basic Identity</div>',
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

    st.write("")

    # ================== STEP 2: GOVERNMENT ID ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="bc-pill">Step 2 · Government ID</div>',
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

    # ================== STEP 3: ADDRESS & FINANCIAL PROFILE ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="bc-pill">Step 3 · Address & Financial Profile</div>',
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

    # ================== FINAL STEP: CONSENT & SUBMIT ==================
    with st.container():
        st.markdown('<div class="bc-card-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="bc-pill">Final Step · Consent & Submit</div>',
            unsafe_allow_html=True
        )

        agree_terms = st.checkbox(
            "I confirm that the information provided is accurate and I agree to BC’s terms, "
            "privacy policy, and KYC / AML checks."
        )

        submitted = st.button("Submit for verification")

        # ---------- SIMPLE COMPLETION LOGIC ----------
        completed_steps = 0
        total_steps = 4  # Step1, Step2, Step3, Consent

        # Step 1 considered done if core identity fields are filled
        if full_name and nationality and residency_country and phone and email:
            completed_steps += 1

        # Step 2 done if files uploaded
        if id_doc is not None and selfie is not None and id_number and id_issue_country:
            completed_steps += 1

        # Step 3 done if address + employment + income filled
        if address_line and city and postal_code and employment_status and income_range:
            completed_steps += 1

        # Consent step
        if agree_terms:
            completed_steps += 1

        progress = int((completed_steps / total_steps) * 100)
        progress_placeholder.progress(progress, text=f"KYC completion: {progress}%")

        # ---------- SUBMIT HANDLING ----------
        if submitted:
            if not agree_terms:
                st.error("Please confirm that the information is accurate and accept the terms to continue.")
            elif not full_name or not email or not id_doc or not selfie:
                st.warning(
                    "Please make sure you filled your name, email, uploaded your ID document and selfie."
                )
            else:
                st.success("✅ KYC submitted. Your profile is now under review. We’ll notify you once it’s verified.")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------- CALL THE FUNCTION ----------
render_kyc_page()
