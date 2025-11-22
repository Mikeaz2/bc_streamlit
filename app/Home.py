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
        box-shadow: 0 12px 30px rgba(0,0
