import streamlit as st
from cerebras_client import call_cerebras

# ---- Adaptive Light/Dark Theme CSS with Mobile Responsiveness ----
st.markdown("""
<style>
/* Import modern fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ============================================
   DEFAULT LIGHT THEME (Base Styles)
   ============================================ */
.stApp, body, .reportview-container, .main {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
    color: #1a1a2e !important;
    transition: background 0.3s ease, color 0.3s ease;
}

/* Sidebar - Light */
section[data-testid="stSidebar"], [data-testid="stSidebarNav"] {
    background: linear-gradient(180deg, #ffffff 0%, #f0f2f5 100%) !important;
    color: #1a1a2e !important;
    border-right: 1px solid #e0e0e0;
}

[data-testid="stSidebar"] .stButton button, 
[data-testid="stSidebar"] .stRadio, 
[data-testid="stSidebar"] label {
    color: #2c3e50 !important;
    font-weight: 600;
}

/* Input Fields - Light */
.stTextArea textarea, .stTextInput input {
    background: #ffffff !important;
    border-radius: 16px;
    color: #1a1a2e !important;
    font-weight: 500;
    border: 2px solid #d1d5db;
    padding: 12px 16px;
    transition: all 0.2s ease;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

/* Headings - Light */
h1, h2, h3, .stSubheader, .stMarkdown {
    color: #1a1a2e !important;
    letter-spacing: -0.02em;
    font-weight: 700;
}

/* Buttons - Light */
.stButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #ffffff !important;
    font-size: 1.05em;
    border-radius: 12px !important;
    font-weight: 600;
    padding: 10px 28px;
    border: none;
    box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
    transition: all 0.25s ease;
    cursor: pointer;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
}

/* Status Messages - Light */
.stSuccess, .stWarning, .stError {
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.9) !important;
    color: #1a1a2e !important;
    font-weight: 500;
    padding: 14px 18px;
    border-left: 4px solid #10b981;
}

.stError {
    border-left-color: #ef4444;
}

/* Dividers - Light */
hr {
    border: none;
    border-top: 2px solid #e5e7eb;
    margin: 1.8em 0 1.2em 0;
}

/* ============================================
   DARK THEME (System Preference)
   ============================================ */
@media (prefers-color-scheme: dark) {
    .stApp, body, .reportview-container, .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%) !important;
        color: #e4e4e7 !important;
    }
    
    /* Sidebar - Dark */
    section[data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        background: linear-gradient(180deg, #16213e 0%, #0f1419 100%) !important;
        color: #e4e4e7 !important;
        border-right: 1px solid #2d3748;
    }
    
    [data-testid="stSidebar"] .stButton button, 
    [data-testid="stSidebar"] .stRadio,
    [data-testid="stSidebar"] label {
        color: #e4e4e7 !important;
    }
    
    /* Input Fields - Dark */
    .stTextArea textarea, .stTextInput input {
        background: #1e293b !important;
        color: #e4e4e7 !important;
        border: 2px solid #334155;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2);
    }
    
    /* Headings - Dark */
    h1, h2, h3, .stSubheader, .stMarkdown {
        color: #f3f4f6 !important;
        text-shadow: 0 2px 12px rgba(129, 140, 248, 0.3);
    }
    
    /* Buttons - Dark */
    .stButton button {
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%) !important;
        box-shadow: 0 4px 14px rgba(129, 140, 248, 0.4);
    }
    
    .stButton button:hover {
        box-shadow: 0 6px 20px rgba(129, 140, 248, 0.6) !important;
    }
    
    /* Status Messages - Dark */
    .stSuccess, .stWarning, .stError {
        background: rgba(30, 41, 59, 0.9) !important;
        color: #e4e4e7 !important;
        border-left-color: #34d399;
    }
    
    .stError {
        border-left-color: #f87171;
    }
    
    /* Dividers - Dark */
    hr {
        border-top: 2px solid #334155;
    }
}

/* ============================================
   MOBILE RESPONSIVE DESIGN
   ============================================ */
@media screen and (max-width: 768px) {
    .stApp {
        padding: 3vw !important;
    }
    
    h1 {
        font-size: 2em !important;
        padding: 12px 0 !important;
    }
    
    .stButton button {
        font-size: 0.95em !important;
        padding: 8px 18px !important;
        width: 100%;
    }
    
    .stTextArea textarea, .stTextInput input {
        font-size: 0.95em !important;
        padding: 10px 12px !important;
    }
    
    /* Stack columns vertically on mobile */
    [data-testid="column"] {
        width: 100% !important;
        margin-bottom: 1.5rem;
    }
}

/* Hide Streamlit branding */
footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---- Page Config ----
st.set_page_config(
    page_title="Meeting Summarizer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Sidebar ----
st.sidebar.title(" Dashboard")
st.sidebar.markdown("---")
option = st.sidebar.radio(
    "Choose input method:",
    ("Upload File", "Paste Text"),
    help="Select how you'd like to provide your meeting transcript"
)

transcript = ""

# ---- Main Header ----
st.markdown("""
<div style='text-align:center; margin-bottom: 2rem;'>
    <h1 style='font-size: 3.2em; 
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 0.3rem;'>
        💬 Meeting Summarizer
    </h1>
    <p style='font-size: 1.2em; opacity: 0.8; font-weight: 500;'>
        Generate intelligent summaries & action items in seconds
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---- Input Section ----
st.subheader(" Input Your Transcript")

col1, col2 = st.columns([1.2, 1.8], gap="large")

with col1:
    if option == "Upload File":
        st.markdown("**Upload a text file containing your meeting transcript:**")
        uploaded_file = st.file_uploader(
            "Choose a .txt file", 
            type=["txt"],
            help="Upload a plain text file with your meeting notes"
        )
        if uploaded_file:
            transcript = uploaded_file.read().decode("utf-8")
            st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    if option == "Paste Text":
        st.markdown("**Paste your meeting transcript below:**")
        transcript = st.text_area(
            "Transcript content", 
            height=280, 
            placeholder="Paste your meeting transcript here...\n\nExample:\nJohn: Let's discuss Q4 goals.\nSarah: I agree, we should focus on...",
            label_visibility="collapsed"
        )

with col2:
    st.info("""
       How to Use:
    
    1. Choose your input method from the sidebar
    2. Upload a file or paste your transcript
    3. Click "Generate Summary" to get AI-powered insights
    
      Tips:
      
    - Include speaker names for better context
    - Longer transcripts yield more detailed summaries
    - Works with any meeting format
    """)

# ---- Results Area ----
if transcript:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(" Analysis Results")
    
    result_col1, result_col2 = st.columns([1, 1], gap="large")
    
    with result_col1:
        st.markdown(" Original Transcript")
        st.text_area(
            "Transcript display", 
            transcript, 
            height=280, 
            disabled=True,
            label_visibility="collapsed"
        )
    
    with result_col2:
        st.markdown(" AI-Generated Summary")
        
        if st.button("✨ Generate Summary", use_container_width=True):
            with st.spinner("🔄 Analyzing transcript and generating summary..."):
                try:
                    summary = call_cerebras(
                        f"Summarize this meeting transcript concisely, highlighting key points and action items:\n\n{transcript}", 
                        max_tokens=300
                    )
                    st.success(summary)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ---- Footer ----
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; padding: 1rem 0; opacity: 0.7;'>
    <p style='margin: 0.3rem 0;'>Built with 🧠 Cerebras AI + Streamlit</p>
    <p style='margin: 0.3rem 0;'>Crafted with 💗 by <strong>P Charmi Reddy</strong></p>
</div>
""", unsafe_allow_html=True)
