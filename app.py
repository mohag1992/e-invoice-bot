"""
e-Invoice Guideline Bot - Web UI
Run: streamlit run app.py
"""

import os
import streamlit as st

from bot_engine import (
    answer_with_openai,
    answer_fallback,
    detect_language,
    load_knowledge_base,
)

st.set_page_config(
    page_title="e-Invoice Guideline Bot",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS – high-contrast text so words are easy to see
st.markdown("""
<style>
    /* Chat and all text: dark color for readability */
    .stChatMessage { padding: 0.5rem 0; }
    .stChatMessage p, .stChatMessage li, .stChatMessage div,
    .stChatMessage span, .stChatMessage strong, .stChatMessage code,
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] div, [data-testid="stChatMessage"] span,
    .stMarkdown p, .stMarkdown li, .stMarkdown div, .stMarkdown span {
        color: #0f172a !important;
    }
    div[data-testid="stMarkdown"] { color: #0f172a !important; }
    [data-testid="stAppViewContainer"] { background: #f1f5f9; }
    .main-header { font-size: 1.6rem; color: #0f172a !important; font-weight: 700; margin-bottom: 0.5rem; }
    .sub-header { color: #334155 !important; font-size: 0.95rem; margin-bottom: 1.5rem; }
    .lang-badge { display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-left: 0.5rem; font-weight: 600; }
    .lang-en { background: #1e40af; color: #fff !important; }
    .lang-ja { background: #9d174d; color: #fff !important; }
    /* Sidebar and captions */
    .stSidebar p, .stSidebar a, .stCaption { color: #0f172a !important; }
    .stSidebar a { color: #1d4ed8 !important; }
</style>
""", unsafe_allow_html=True)

kb = load_knowledge_base()
has_kb = bool(kb)
use_ai = bool(os.environ.get("OPENAI_API_KEY"))

st.markdown('<p class="main-header">📄 e-Invoice Guideline Bot</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">IRBM e-Invoice Guideline (v4.6) に基づく質問に、英語・日本語で回答します / Answers based on the official guideline in English or Japanese.</p>',
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("lang"):
            badge = "lang-ja" if msg["lang"] == "ja" else "lang-en"
            label = "日本語" if msg["lang"] == "ja" else "English"
            st.markdown(f'<span class="lang-badge {badge}">{label}</span>', unsafe_allow_html=True)

prompt = st.chat_input("Ask about e-Invoice (English or 日本語) / e-Invoiceについて質問（英語・日本語）")

if prompt:
    lang = detect_language(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "lang": lang})
    with st.chat_message("user"):
        st.markdown(prompt)
        badge = "lang-ja" if lang == "ja" else "lang-en"
        label = "日本語" if lang == "ja" else "English"
        st.markdown(f'<span class="lang-badge {badge}">{label}</span>', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("Searching guideline..." if lang == "en" else "ガイドラインを参照しています..."):
            if use_ai:
                answer = answer_with_openai(prompt)
            else:
                answer = answer_fallback(prompt)
                if has_kb:
                    st.caption(
                        "Tip: Set OPENAI_API_KEY for full AI answers in your language."
                        if lang == "en"
                        else "ヒント: OPENAI_API_KEY を設定すると、AIが言語に合わせて回答します。"
                    )
        st.markdown(answer)
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "lang": lang,
        })

with st.sidebar:
    st.header("About")
    st.markdown(
        "Answers are based on **IRBM e-Invoice Guideline (Version 4.6)** "
        "(Publication: 7 December 2025)."
    )
    st.markdown("[Guideline PDF](https://www.hasil.gov.my/media/fzagbaj2/irbm-e-invoice-guideline.pdf)")
    st.markdown("[MyTax Portal](https://mytax.hasil.gov.my)")
    st.divider()
    st.caption("Language is auto-detected from your question. Responds in 日本語 or English.")
