import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="BC – Borderless Credit",
    page_icon="app/assets/bc-logo.png",  # logo as favicon
    layout="wide"
)

# ---------- LIGHT CUSTOM STYLING ----------
st.markdown(
    """
    <style>
    /* Make the main page a bit more "landing page" like */
    .main {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Centered hero content */
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.25rem;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        text-align: center;
        color: #A0AEC0;
        margin-bottom: 1.5rem;
    }

    /* Section titles */
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    /* Simple "card" styling */
    .bc-card {
        background: #0b1220;
        border-radius: 16px;
        padding: 1.1rem 1.25rem;
        border: 1px solid rgba(57, 208, 200, 0.25);
        box-shadow: 0 12px 30px rgba(0,0,0,0.35);
        height: 100%;
    }
    .bc-card h4 {
        margin-bottom: 0.4rem;
        font-size: 1.05rem;
    }
    .bc-tag {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        background: rgba(57,208,200,0.12);
        color: #39D0C8;
        font-size: 0.8rem;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
    }

    /* Make markdown lists a bit tighter */
    .element-container ul {
        margin-top: 0.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HERO SECTION ----------
hero_col1, hero_col2, hero_col3 = st.columns([1, 2, 1])
with hero_col2:
    st.image("app/assets/bc-logo.png", width=180)

st.markdown('<div class="hero-title">BC – Borderless Credit</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AI-powered, borderless credit identities for students, freelancers, and immigrants.</div>', unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; color:#A0AEC0;'>"
    "This prototype shows how BC turns fragmented financial data into a <strong>portable global credit score</strong> "
    "that travels with you across borders."
    "</p>",
    unsafe_allow_html=True,
)

st.divider()

# ---------- SECTION 1: WHAT BC SOLVES ----------
sec1_col1, sec1_col2, sec1_col3 = st.columns([1.1, 1.1, 1.1])
with sec1_col1:
    st.markdown('<div class="bc-card">', unsafe_allow_html=True)
    st.markdown("#### 🌍 Problem", unsafe_allow_html=True)
    st.write(
        "Credit systems are national, but people are global. When someone moves countries, "
        "their credit history usually doesn’t follow, forcing them to start from zero."
    )
    st.markdown("</div>", unsafe_allow_html=True)

with sec1_col2:
    st.markdown('<div class="bc-card">', unsafe_allow_html=True)
    st.markdown("#### 🧠 Our Approach", unsafe_allow_html=True)
    st.write(
        "BC aggregates open-banking data, mobile-money flows, gig income, rent, utilities, "
        "and remittances into a single global profile, scored by our machine-learning engine."
    )
    st.markdown("</div>", unsafe_allow_html=True)

with sec1_col3:
    st.markdown('<div class="bc-card">', unsafe_allow_html=True)
    st.markdown("#### ✅ Outcome", unsafe_allow_html=True)
    st.write(
        "A portable BC Score that lenders in multiple countries can read via API, "
        "unlocking micro-loans, housing, tuition finance, and working capital for people who were previously credit-invisible."
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("")  # small spacing

# ---------- SECTION 2: DEMO FLOW ----------
st.markdown('<div class="section-title">Prototype Flow</div>', unsafe_allow_html=True)
flow_col1, flow_col2 = st.columns([1.2, 1])

with flow_col1:
    st.markdown(
        """
        1. **Onboarding & KYC** – user signs up and passes a simulated digital KYC check.  
        2. **Link Accounts** – bank, mobile-money, or CSV data are connected to BC.  
        3. **ML-Driven Scoring** – the engine computes a portable BC Score from cash-flows and alternative data.  
        4. **Micro-Loan Offer** – the user sees an instant, transparent loan offer based on their risk band.  
        5. **Lender Portal View** – a partner lender can inspect key risk signals behind the score.
        """,
    )
    st.info("Use the left sidebar to walk through each step of this flow in the prototype.", icon="👈")

with flow_col2:
    st.markdown('<div class="bc-card">', unsafe_allow_html=True)
    st.markdown("#### Who BC Is Built For", unsafe_allow_html=True)
    st.markdown(
        """
        - International students  
        - Migrant workers & new arrivals  
        - Freelancers & gig-platform earners  
        - Digital nomads and remote professionals  
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("")

# ---------- SECTION 3: TARGET USERS & VALUE ----------
st.markdown('<div class="section-title">Why BC Matters</div>', unsafe_allow_html=True)
val_col1, val_col2, val_col3 = st.columns([1.1, 1.1, 1.1])

with val_col1:
    st.markdown('<div class="bc-card">', unsafe_allow_html=True)
    st.markdown("#### For Borrowers", unsafe_allow_html=True)
    st.write(
        "- Carry your creditworthiness across borders\n"
        "- Access fair credit earlier in a new country\n"
        "- Turn everyday financial behavior into opportunity"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with val_col2:
    st.markdown('<div class="bc-card">', unsafe_allow_html=True)
    st.markdown("#### For Lenders", unsafe_allow_html=True)
    st.write(
        "- Lower information asymmetry\n"
        "- Faster onboarding via open-banking and APIs\n"
        "- New, underserved customer segments with data-backed risk"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with val_col3:
    st.markdown('<div class="bc-card">', unsafe_allow_html=True)
    st.markdown("#### For the System", unsafe_allow_html=True)
    st.write(
        "- Expands financial inclusion\n"
        "- Uses technology to reduce friction and search costs\n"
        "- Aligns with global open-finance and responsible-AI trends"
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("")

# ---------- SECTION 4: TAGS / POSITIONING ----------
st.markdown('<div class="section-title">BC in One Line</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:1.05rem; color:#E2E8F0;'>"
    "<strong>BC is a global, machine-learning powered infrastructure for portable credit identities.</strong>"
    "</p>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <span class="bc-tag">Open Banking</span>
    <span class="bc-tag">Alternative Data</span>
    <span class="bc-tag">Financial Inclusion</span>
    <span class="bc-tag">Cross-Border Lending</span>
    <span class="bc-tag">AI Credit Scoring</span>
    """,
    unsafe_allow_html=True,
)
