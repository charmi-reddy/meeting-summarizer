import streamlit as st
from cerebras_client import call_cerebras

# ---- Universal Dark & Mobile-responsive CSS ----
st.markdown("""
<style>
.stApp, body, .reportview-container, .main {
    background: #000 !important;
    font-family: 'Roboto Mono', 'JetBrains Mono', 'Montserrat', sans-serif;
    color: #fff !important;
}

section[data-testid="stSidebar"], [data-testid="stSidebarNav"] {
    background: #111 !important;
    color: #fff !important;
}

[data-testid="stSidebar"] .stButton button, 
[data-testid="stSidebar"] .stRadio, 
[data-testid="stSidebar"] .stFileUploader, 
[data-testid="stSidebar"] .stSubheader {
    color: #fff !important;
    font-weight: bold;
}

.stTextArea textarea, .stTextInput input {
    background: #222 !important;
    border-radius: 18px;
    color: #fff !important;
    font-weight: bold;
    border: 2px solid #333;
}

h1, h2, .stSubheader, .stMarkdown {
    color: #fff !important;
    text-shadow: 0 2px 10px #222;
    letter-spacing: 0.04em;
}

.stButton button {
    background: #181818 !important;
    color: #fff !important;
    font-size: 1.1em;
    border-radius: 14px !important;
    font-weight: 700;
    box-shadow: 0 2px 8px #333;
    transition: box-shadow 0.2s;
    border: 1.5px solid #333;
    padding: 8px 22px;
}

.stButton button:hover {
    box-shadow: 0 4px 16px #444 !important;
    border: 2px solid #fff !important;
}

.stSuccess, .stWarning, .stError {
    border-radius: 18px;
    background: #1a1a1a !important;
    color: #fff !important;
    font-weight: 600;
    font-size: 1.1em;
}

hr {
    border: none;
    border-top: 2px solid #333;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

footer {
    visibility: hidden;
}

/* Responsive mobile tweaks */
@media screen and (max-width: 650px) {
    .stApp {
        padding: 2vw !important;
    }
    h1, .stMarkdown h1 {
        font-size: 2em !important;
        padding: 14px 0 !important;
        border-radius: 18px !important;
    }
    .stButton button {
        font-size: 1em !important;
        padding: 6px 14px !important;
    }
    .stTextArea textarea, .stTextInput input {
        font-size: 1em !important;
        padding: 8px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ---- Page Config ----
st.set_page_config(
    page_title="Meeting Summarizer",
    page_icon="💗",
    layout="wide"
)

# ---- Sidebar ----
st.sidebar.header("Dashboard")
option = st.sidebar.radio(
    "Choose input method:",
    ("Upload File", "Paste Text")
)

transcript = ""

# ---- Main/Header ----
st.markdown("""
<h1 style='text-align:center;
            background: #181818;
            color:#fff;
            border-radius:22px;
            margin-top:-18px;
            padding:16px 0;
            font-size:3em;
            text-shadow:0 6px 24px #222;'>
 MEETING SUMMARIZER 3000 
</h1>
""", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;font-size:1.28em;color:#eaeaec;'>
Generate dazzling summaries & futuristic action items in seconds<br>
<span style='color:#ff4b6e;font-weight:900;'>AI-Powered. Neon-Polished. Super Fast.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---- Input Area (Glassmorphism Block with Modern Dark Look) ----
glass_style = """
<div style='background:rgba(26,24,58,0.35);
            box-shadow:0 4px 32px #3c267c33;
            border-radius:22px;
            padding:18px 4vw 22px 4vw;
            margin-bottom:24px;'>
"""

col1, col2 = st.columns([1.1, 1.9])

with col1:
    if option == "Upload File":
        uploaded_file = st.file_uploader("Upload your transcript (.txt)", type=["txt"])
        if uploaded_file:
            transcript = uploaded_file.read().decode("utf-8")
    if option == "Paste Text":
        transcript = st.text_area("Paste here", height=260, placeholder="Paste your meeting transcript...", key="paste_area")

with col2:
    st.markdown(f"{glass_style}<b style='font-size:1.13em;color:#dfeff7;'>Instructions:</b><br>Upload or paste your transcript.</div>", unsafe_allow_html=True)

# ---- Results Area ----
if transcript:
    out_col1, out_col2 = st.columns([1.15, 1.25])
    with out_col1:
        st.markdown(f"{glass_style}<span style='font-size:1.18em;color:#ffa4ff;font-weight:700;'>Transcript</span></div>", unsafe_allow_html=True)
        st.text_area("", transcript, height=200, disabled=True)
    with out_col2:
        st.markdown(f"{glass_style}<span style='font-size:1.18em;color:#2dffef;font-weight:700;'>AI Summary</span></div>", unsafe_allow_html=True)
        if option != "Demo Transcript" or st.session_state.get("demo_summary") == "":
            if st.button("Generate Summary"):
                with st.spinner("Generating futuristic summary..."):
                    try:
                        summary = call_cerebras(f"Summarize this meeting transcript:\n\n{transcript}", max_tokens=300)
                        st.success(summary)
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.success(st.session_state["demo_summary"])

# ---- Footer ----
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;color:#ffeaf9;font-size:1.03em;margin-bottom:14px;'>
<span style='font-size:1.09em;'>Built with Cerebras + Streamlit</span> <br>
<span style='font-size:1.09em;'>Made with 💗 by P Charmi Reddy</span>
</div>
""", unsafe_allow_html=True)
