import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="BC – Borderless Credit",
    page_icon="app/assets/bc-logo.png",
    layout="wide"
)

# ---------- LIGHT CUSTOM STYLING ----------
st.markdown(
    """
    <style>
    .main {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Header */
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

    /* Card containers */
    .bc-card {
        background: #0b1220;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        border: 1px solid rgba(57, 208, 200, 0.25);
        box-shadow: 0 10px 26px rgba(0,0,0,0.35);
        height: 100%;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 600;
        margin: 1.4rem 0 0.6rem 0;
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
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HEADER (LOGO + TITLE LEFT ALIGNED) ----------
header_logo_col, header_text_col, _ = st.columns([0.6, 3, 0.5])

with header_logo_col:
    # bigger logo
    st.image("app/assets/bc-logo.png", width=300)

with header_text_col:
    st.markdown('<div class="bc-header-title">BC – Borderless Credit</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="bc-header-subtitle">'
        'AI-powered, borderless credit identities for students, freelancers, and immigrants.'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "This prototype shows how BC turns fragmented financial data into a "
        "**portable global credit score** that travels with you across borders."
    )

st.divider()

# ---------- SMALL HELPER FOR CARDS WITH TITLE PILLS ----------
def card(title: str, content: str) -> str:
    return f"""
        <div class="bc-card">
            <div style="
                background: rgba(57, 208, 200, 0.10);
                border-radius: 10px;
                padding: 6px 10px;
                font-weight: 600;
                margin-bottom: 0.6rem;
            ">
                {title}
            </div>
            <div style="font-size:0.95rem; line-height:1.45;">
                {content}
            </div>
        </div>
    """

# ---------- PROBLEM / APPROACH / OUTCOME CARDS ----------
st.markdown('<div class="section-title">What BC Does</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(card(
        "Problem",
        "Credit systems are national, but people are global. When someone moves countries, "
        "their credit history usually doesn’t follow, forcing them to start from zero in the new market."
    ), unsafe_allow_html=True)

with c2:
    st.markdown(card(
        "Our Approach",
        "BC aggregates open-banking data, mobile-money flows, gig income, rent, utilities, "
        "and remittances into a single global profile, scored by a machine-learning engine."
    ), unsafe_allow_html=True)

with c3:
    st.markdown(card(
        "Outcome",
        "A portable BC Score that lenders in multiple countries can read via API, unlocking micro-loans, "
        "housing, tuition finance, and working capital for people who were previously credit-invisible."
    ), unsafe_allow_html=True)

# ---------- PROTOTYPE FLOW ----------
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
        """
    )
    st.info("Use the left sidebar to walk through each step of this flow in the prototype.", icon="👈")

with flow_col2:
    st.markdown(card(
        "Who BC Is Built For",
        """
        - International students  
        - Migrant workers & new arrivals  
        - Freelancers & gig-platform earners  
        - Digital nomads and remote professionals  
        """
    ), unsafe_allow_html=True)

# ---------- VALUE SECTION ----------
st.markdown('<div class="section-title">Why BC Matters</div>', unsafe_allow_html=True)

val1, val2, val3 = st.columns(3)

with val1:
    st.markdown(card(
        "For Borrowers",
        "- Carry your creditworthiness across borders<br>"
        "- Access fair credit earlier in a new country<br>"
        "- Turn everyday financial behavior into opportunity"
    ), unsafe_allow_html=True)

with val2:
    st.markdown(card(
        "For Lenders",
        "- Lower information asymmetry<br>"
        "- Faster onboarding via open-banking and APIs<br>"
        "- New, underserved customer segments with data-backed risk"
    ), unsafe_allow_html=True)

with val3:
    st.markdown(card(
        "For the System",
        "- Expands financial inclusion<br>"
        "- Uses technology to reduce friction and search costs<br>"
        "- Aligns with global open-finance and responsible-AI trends"
    ), unsafe_allow_html=True)

# ---------- TAGLINE ----------
st.markdown('<div class="section-title">BC in One Line</div>', unsafe_allow_html=True)
st.markdown(
    "**BC is a global, machine-learning powered infrastructure for portable credit identities.**"
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
