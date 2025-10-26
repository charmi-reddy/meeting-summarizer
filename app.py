import streamlit as st
from cerebras_client import call_cerebras

# ---- Futuristic CSS ----
st.markdown("""
<style>
body, .reportview-container, .main {
    background: linear-gradient(120deg, #182848 0%, #ffa4ff 100%);
    font-family: 'Roboto Mono', 'JetBrains Mono', 'Montserrat', sans-serif;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(120deg, #2d185c 0%, #6a4b9b 100%);
    color: #fff;
}
[data-testid="stSidebar"] .stButton button, [data-testid="stSidebar"] .stRadio, [data-testid="stSidebar"] .stFileUploader, [data-testid="stSidebar"] .stSubheader {
    color: #fff !important;
    font-weight: bold;
}
.stTextArea textarea, .stTextInput input {
    background: rgba(255,255,250,0.12);
    border-radius: 18px;
    color: #fff;
    font-weight: bold;
    border: 2px solid #ff4b6e;
}
h1, h2, .stSubheader, .stMarkdown {
    text-shadow: 0 2px 10px #ff85ff88;
    letter-spacing: 0.04em;
}
.stButton button {
    background: linear-gradient(90deg, #ff4b6e 0%, #ffa4ff 100%);
    color: #fff;
    font-size: 1.1em;
    border-radius: 14px !important;
    font-weight: 700;
    box-shadow: 0 2px 8px #db34c431;
    transition: box-shadow 0.2s;
}
.stButton button:hover {
    box-shadow: 0 4px 16px #fc96c7cc;
    border: 2px solid #fff;
}
.stSuccess, .stWarning, .stError {
    border-radius: 18px;
    background: rgba(255,255,255,0.13);
    color: #fff !important;
    font-weight: 600;
    font-size: 1.1em;
}
hr {
    border: none;
    border-top: 2px solid #ff4b6e;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}
footer {
    visibility: hidden;
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
            background: linear-gradient(90deg,#fdc9f0 0%,#a18fff 65%);
            color:#fff;
            border-radius:22px;
            margin-top:-18px;
            padding:16px 0;
            font-size:3em;
            text-shadow:0 6px 24px #cb7cfbcc;'>
 MEETING SUMMARIZER 3000 
</h1>
""", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;font-size:1.35em;color:#f0f2fa;'>
Generate dazzling summaries & futuristic action items in seconds<br>
<span style='color:#ff4b6e;font-weight:900;'>AI-Powered. Neon-Polished. Super Fast.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---- Input Area (Ultra-wide, Glassmorphism Block) ----
glass_style = """
<div style='background:rgba(26,24,58,0.25);
            box-shadow:0 4px 44px #c097fc40;
            border-radius:22px;
            padding:28px 34px 38px 34px;
            margin-bottom:28px;'>
"""

col1, col2 = st.columns([1.1, 1.9])

with col1:
    if option == "Upload File":
        uploaded_file = st.file_uploader("Upload your transcript (.txt)", type=["txt"])
        if uploaded_file:
            transcript = uploaded_file.read().decode("utf-8")
    if option == "Paste Text":
        transcript = st.text_area("Paste here", height=340, placeholder="Paste your meeting transcript...", key="paste_area")

with col2:
    st.markdown(f"{glass_style}<b style='font-size:1.13em;color:#dfeff7;'>Instructions:</b><br>Upload or paste your transcript.", unsafe_allow_html=True)

# ---- Results Area ----
if transcript:
    out_col1, out_col2 = st.columns([1.15, 1.25])
    with out_col1:
        st.markdown(f"{glass_style}<span style='font-size:1.22em;color:#ffa4ff;font-weight:700;'>Transcript</span></div>", unsafe_allow_html=True)
        st.text_area("", transcript, height=320, disabled=True)
    with out_col2:
        st.markdown(f"{glass_style}<span style='font-size:1.22em;color:#2dffef;font-weight:700;'>AI Summary</span></div>", unsafe_allow_html=True)
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
<div style='text-align:center;color:#ffeaf9;font-size:1.03em;margin-bottom:7px;'>
<span style='font-size:1.09em;'>Built with Cerebras + Streamlit</span> \n
<span style='font-size:1.09em;'>Made with 💗 by P Charmi Reddy</span>
</div>
""", unsafe_allow_html=True)
