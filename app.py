import streamlit as st
from cerebras_client import call_cerebras
from datetime import datetime

# ---- Initialize Session State for History ----
if 'summary_history' not in st.session_state:
    st.session_state['summary_history'] = []

if 'show_sidebar' not in st.session_state:
    st.session_state['show_sidebar'] = True

# ---- Hamburger Menu & Responsive CSS ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp, body, .reportview-container, .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #212529 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    [data-testid="block-container"] {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    #hamburger {
        position: fixed;
        top: 18px;
        left: 22px;
        z-index: 99998;
        width: 44px;
        height: 44px;
        background: #fff;
        border: 1.5px solid #ddd;
        border-radius: 50%;
        box-shadow: 0 2px 16px rgba(102,126,234,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: border 0.2s, box-shadow 0.2s;
    }
    #hamburger:hover {
        border: 1.5px solid #6366f1;
        box-shadow: 0 4px 16px rgba(99,102,241,0.17);
    }
    #ham-bar1, #ham-bar2, #ham-bar3 {
        display: block;
        width: 21px;
        height: 3.2px;
        margin: 3px 0;
        background: #667eea;
        border-radius: 3px;
        transition: 0.3s;
    }
    @media (max-width: 768px) {
        #hamburger { top: 10px; left: 12px; width: 38px; height: 38px; }
        [data-testid="block-container"] { padding-top: 1rem !important; }
    }
    /* Hide hamburger if sidebar is open */
    [data-testid="stSidebar"][aria-expanded="true"] ~ div > #hamburger {
        display: none !important;
    }
    /* Dark mode hamburger background */
    @media (prefers-color-scheme: dark) {
        #hamburger { background: #161b22; border-color: #30363d; }
        #ham-bar1, #ham-bar2, #ham-bar3 { background: #818cf8; }
    }
    </style>
""", unsafe_allow_html=True)

# ---- Hamburger UI & Logic ----
sidebar_toggle_script = """
    <script>
    function toggleSidebar() {
        var sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if(sidebar){
            sidebar.setAttribute('aria-expanded',
                sidebar.getAttribute('aria-expanded')=='true' ? 'false' : 'true')
        }
    }
    document.addEventListener("DOMContentLoaded", function(){
        document.getElementById("hamburger").onclick = toggleSidebar;
    });
    </script>
"""
st.markdown("""
    <div id="hamburger" title="Open dashboard">
      <span id="ham-bar1"></span>
      <span id="ham-bar2"></span>
      <span id="ham-bar3"></span>
    </div>
"""+sidebar_toggle_script, unsafe_allow_html=True)

# ---- Page Config ----
st.set_page_config(
    page_title="Meeting Summarizer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Sidebar ----
with st.sidebar:
    st.title("Dashboard")
    st.radio(
        "Input Method",
        ("Upload File", "Paste Text"),
        key="input_method",
        help="Select how you'd like to provide your meeting transcript"
    )
    st.markdown("---")
    st.subheader("Summary History")
    if st.session_state['summary_history']:
        for idx, item in enumerate(reversed(st.session_state['summary_history'])):
            with st.expander(f"{item['timestamp']}", expanded=False):
                st.markdown("**Transcript Preview**")
                st.text(item['transcript'][:100] + "...")
                st.markdown("**Summary**")
                st.info(item['summary'])
    else:
        st.info("No summaries generated yet")
    # Clear History Button
    if st.session_state['summary_history']:
        if st.button("Clear History", use_container_width=True):
            st.session_state['summary_history'] = []
            st.rerun()

transcript = ""

# ---- Main Header ----
st.markdown("""
<div style='text-align:center; margin-bottom: 2.5rem;'>
    <h1 style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 0.5rem;'>
        Meeting Summarizer
    </h1>
    <p style='font-size: 1.15rem; opacity: 0.75; font-weight: 400; margin-top: 0;'>
        Generate intelligent summaries and action items in seconds
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---- Input Section ----
st.subheader("Input Your Transcript")

col1, col2 = st.columns([1.2, 1.8], gap="large")
option = st.session_state.get("input_method", "Paste Text")

with col1:
    if option == "Upload File":
        st.markdown("**Upload your meeting transcript**")
        uploaded_file = st.file_uploader(
            "Choose a .txt file", 
            type=["txt"],
            help="Upload a plain text file with your meeting notes"
        )
        if uploaded_file:
            transcript = uploaded_file.read().decode("utf-8")
            st.success(f"File uploaded successfully: {uploaded_file.name}")
    if option == "Paste Text":
        st.markdown("**Paste your meeting transcript**")
        transcript = st.text_area(
            "Transcript content", 
            height=300, 
            placeholder=(
                "Paste your meeting transcript here...\n\n"
                "Example:\nJohn: Let's discuss Q4 goals.\nSarah: I agree, we should focus on customer retention."
            ),
            label_visibility="collapsed",
            key="transcript_input"
        )
with col2:
    st.info(
        "**How to Use**\n"
        "1. Choose your input method from the dashboard\n"
        "2. Upload a file or paste your transcript\n"
        "3. Click 'Generate Summary' to get AI-powered insights\n"
        "4. View previous summaries in the history section\n\n"
        "**Tips**\n"
        "* Include speaker names for better context\n"
        "* Longer transcripts yield more detailed summaries\n"
        "* Works with any meeting format"
    )

# ---- Results Area ----
if transcript:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Analysis Results")
    result_col1, result_col2 = st.columns([1, 1], gap="large")
    with result_col1:
        st.markdown("**Original Transcript**")
        st.text_area(
            "Transcript display", 
            transcript, 
            height=300, 
            disabled=True,
            label_visibility="collapsed"
        )
    with result_col2:
        st.markdown("**AI-Generated Summary**")
        if st.button("Generate Summary", use_container_width=True, key="generate_btn"):
            with st.spinner("Analyzing transcript and generating summary..."):
                try:
                    summary = call_cerebras(
                        f"Summarize this meeting transcript concisely, highlighting key points and action items:\n\n{transcript}", 
                        max_tokens=300
                    )
                    st.session_state['summary_history'].append({
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'transcript': transcript,
                        'summary': summary
                    })
                    st.success(summary)
                except Exception as e:
                    st.error(f"Error: {e}")

# ---- Footer ----
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; padding: 1rem 0; opacity: 0.6; font-size: 0.9rem;'>
    <p style='margin: 0.2rem 0;'>Built with Cerebras AI and Streamlit</p>
    <p style='margin: 0.2rem 0;'>Crafted by P Charmi Reddy</p>
</div>
""", unsafe_allow_html=True)
