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
    st.image("app/assets/bc-logo.png", width=120)

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
            <div style="font-size:0.95rem; line-he
