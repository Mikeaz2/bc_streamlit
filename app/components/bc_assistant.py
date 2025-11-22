import streamlit as st


def _init_assistant_state():
    if "bc_assistant_open" not in st.session_state:
        st.session_state["bc_assistant_open"] = False
    if "bc_assistant_msgs" not in st.session_state:
        st.session_state["bc_assistant_msgs"] = [
            {
                "role": "assistant",
                "content": (
                    "Hi, I’m the **BC AI Assistant**.\n\n"
                    "You can ask me things like:\n"
                    "- *Why is my BC AI score like this?*\n"
                    "- *How can I improve my credit limit?*\n"
                    "- *Why was my micro-loan partially approved?*\n"
                    "- *What do my risk flags mean?*"
                ),
            }
        ]


def _bc_generate_reply(user_message: str) -> str:
    """Very simple, rule-based explanation engine for the prototype."""
    text = user_message.lower()

    # Default generic reply
    reply = (
        "BC’s AI looks at a mix of factors: your **income stability**, "
        "**volatility of cash flows**, **utilization**, **missed payments**, and "
        "**jurisdiction risk**. Based on that, it produces your score, risk band, "
        "and a suggested credit limit.\n\n"
        "You can usually improve your profile by:\n"
        "- Reducing income volatility\n"
        "- Keeping utilization in a healthy range (around 10–40%)\n"
        "- Avoiding missed or late payments\n"
        "- Linking more accounts to give BC more history to work with."
    )

    if "score" in text or "ai score" in text:
        reply = (
            "Your **BC AI score** is a synthetic score between **300 and 900**.\n\n"
            "In your prototype, it’s driven by:\n"
            "- Stable monthly income → pushes the score up\n"
            "- Income volatility → higher volatility pulls it down\n"
            "- Credit / wallet utilization → healthy usage is rewarded, very high usage is penalized\n"
            "- Missed or late payments → directly reduce the score\n"
            "- Country / jurisdiction risk → low-risk markets get a small boost\n"
            "- Data depth → more months of history and more linked accounts increase confidence\n\n"
            "The app then turns this score into a **risk band** (Low / Medium / High) "
            "and a suggested limit."
        )

    if "limit" in text or "credit limit" in text or "micro-loan" in text:
        reply = (
            "BC estimates your **credit limit** from two main things:\n"
            "1. Your **stable monthly income** → sets a baseline capacity to repay.\n"
            "2. Your **AI score** → adjusts that capacity up or down based on risk.\n\n"
            "Roughly speaking, the prototype multiplies your income by a factor, then scales it "
            "between **300 and 900** points of risk.\n"
            "A higher score and more stable behavior mean a higher suggested limit and better loan offers."
        )

    if "improve" in text or "increase" in text or "upgrade" in text:
        reply = (
            "You can improve your BC profile over time by:\n"
            "- Keeping your utilization moderate (not maxing out your limit all the time)\n"
            "- Reducing income volatility where possible (more stable gigs or salary)\n"
            "- Avoiding missed or late repayments\n"
            "- Linking more accounts and keeping them active (so BC sees a deeper history)\n"
            "- Operating mostly in lower-risk jurisdictions when possible.\n\n"
            "In the prototype, try adjusting the sliders on the **AI Credit Dashboard** and "
            "watch how your score and suggested limit change."
        )

    if "flags" in text or "risk" in text or "why was i declined" in text or "declined" in text:
        reply = (
            "Risk flags are BC’s way of explaining *why* your profile is cautious:\n\n"
            "- **High income volatility** → your cash flows jump up and down a lot.\n"
            "- **Thin file** → not enough months of history or linked accounts.\n"
            "- **High utilization** → you’re using most of your available limit.\n"
            "- **Missed payments** → you’ve had late or missed repayments.\n"
            "- **Jurisdiction risk** → your main income comes from higher-risk markets.\n\n"
            "These do not mean you are rejected forever — they just explain why the "
            "limit might be lower or why a loan might require manual review."
        )

    if "lender" in text or "lender portal" in text or "investor" in text:
        reply = (
            "For lenders, BC aggregates many users into a **portfolio view** with:\n"
            "- AI scores & risk bands\n"
            "- Volatility measures\n"
            "- Simple transaction histories\n"
            "- Suggested maximum exposures per borrower.\n\n"
            "That lets lenders filter by risk, simulate disbursements, and decide "
            "where to allocate capital while still serving underbanked users."
        )

    return reply


def render_bc_assistant():
    """Render a floating chat assistant bottom-right on the screen."""
    _init_assistant_state()

    # Global CSS for floating container
    st.markdown(
        """
        <style>
        #bc-assistant-container {
            position: fixed;
            bottom: 1.2rem;
            right: 1.2rem;
            width: 340px;
            z-index: 9999;
        }
        .bc-assistant-box {
            background: #020617;
            border-radius: 16px;
            border: 1px solid #1f2937;
            box-shadow: 0 0 18px rgba(0,0,0,0.45);
            padding: 0.7rem 0.8rem 0.9rem 0.8rem;
        }
        .bc-assistant-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.5rem;
        }
        .bc-assistant-title {
            font-weight: 600;
            font-size: 0.95rem;
        }
        .bc-assistant-badge {
            font-size: 0.7rem;
            padding: 0.15rem 0.4rem;
            border-radius: 999px;
            background: #0f172a;
            border: 1px solid #1f2937;
            color: #e5e7eb;
        }
        .bc-assistant-toggle-btn button {
            border-radius: 999px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Container with fixed position
    with st.container():
        st.markdown('<div id="bc-assistant-container">', unsafe_allow_html=True)

        # Closed state -> just a pill button
        if not st.session_state["bc_assistant_open"]:
            col1, col2 = st.columns([1, 0.0001])
            with col1:
                if st.button("💬 BC Assistant", key="bc_open_btn"):
                    st.session_state["bc_assistant_open"] = True
            st.markdown("</div>", unsafe_allow_html=True)
            return

        # Open state -> full chat box
        st.markdown('<div class="bc-assistant-box">', unsafe_allow_html=True)

        # Header with close button
        head_col1, head_col2 = st.columns([4, 1])
        with head_col1:
            st.markdown(
                '<div class="bc-assistant-header">'
                '<div class="bc-assistant-title">BC AI Assistant</div>'
                '<span class="bc-assistant-badge">beta · prototype</span>'
                "</div>",
                unsafe_allow_html=True,
            )
        with head_col2:
            if st.button("✕", key="bc_close_btn"):
                st.session_state["bc_assistant_open"] = False
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                return

        # Chat history
        for msg in st.session_state["bc_assistant_msgs"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input
        user_input = st.chat_input(
            "Ask about your BC score, loan, or risk flags…",
            key="bc_chat_input",
        )

        if user_input:
            st.session_state["bc_assistant_msgs"].append(
                {"role": "user", "content": user_input}
            )
            with st.chat_message("user"):
                st.markdown(user_input)

            reply = _bc_generate_reply(user_input)
            st.session_state["bc_assistant_msgs"].append(
                {"role": "assistant", "content": reply}
            )
            with st.chat_message("assistant"):
                st.markdown(reply)

        st.markdown("</div>", unsafe_allow_html=True)  # close assistant-box
        st.markdown("</div>", unsafe_allow_html=True)  # close container div
