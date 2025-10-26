import streamlit as st
from cerebras_client import call_cerebras
from datetime import datetime

# ---- Initialize Session State for History ----
if 'summary_history' not in st.session_state:
    st.session_state['summary_history'] = []

# ---- Professional Adaptive Theme with Enhanced UX ----
st.markdown("""
<style>
/* Import modern fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ============================================
   LIGHT THEME (Default)
   ============================================ */
.stApp, body, .reportview-container, .main {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: #212529 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Reduced top padding for cleaner look */
[data-testid="block-container"] {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* Sidebar - Light */
section[data-testid="stSidebar"], [data-testid="stSidebarNav"] {
    background: #ffffff !important;
    color: #212529 !important;
    border-right: 1px solid #dee2e6;
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.04);
}

[data-testid="stSidebar"] .stButton button, 
[data-testid="stSidebar"] .stRadio, 
[data-testid="stSidebar"] label {
    color: #495057 !important;
    font-weight: 500;
}

/* Input Fields - Light */
.stTextArea textarea, .stTextInput input {
    background: #ffffff !important;
    border-radius: 12px;
    color: #212529 !important;
    font-weight: 400;
    border: 2px solid #e9ecef;
    padding: 14px 18px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    line-height: 1.6;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.12);
    outline: none;
}

/* Headings - Light */
h1, h2, h3, .stSubheader, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #1a202c !important;
    letter-spacing: -0.025em;
    font-weight: 700;
    line-height: 1.2;
}

h1 { font-size: 2.5rem !important; }
h2 { font-size: 1.75rem !important; margin-top: 1.5rem !important; }
h3 { font-size: 1.25rem !important; }

/* Buttons - Light with microinteraction */
.stButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #ffffff !important;
    font-size: 1rem;
    border-radius: 10px !important;
    font-weight: 600;
    padding: 12px 32px;
    border: none;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    letter-spacing: 0.02em;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.45) !important;
}

.stButton button:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3) !important;
}

/* File Uploader Styling */
[data-testid="stFileUploader"] {
    background: #f8f9fa;
    border: 2px dashed #ced4da;
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.25s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #6366f1;
    background: #f0f1ff;
}

/* Status Messages - Light */
.stSuccess {
    border-radius: 12px;
    background: #d1fae5 !important;
    color: #065f46 !important;
    font-weight: 500;
    padding: 16px 20px;
    border-left: 4px solid #10b981;
    line-height: 1.6;
}

.stError {
    border-radius: 12px;
    background: #fee2e2 !important;
    color: #991b1b !important;
    font-weight: 500;
    padding: 16px 20px;
    border-left: 4px solid #ef4444;
}

.stInfo {
    border-radius: 12px;
    background: #dbeafe !important;
    color: #1e40af !important;
    font-weight: 400;
    padding: 16px 20px;
    border-left: 4px solid #3b82f6;
    line-height: 1.7;
}

/* Dividers - Light */
hr {
    border: none;
    border-top: 1px solid #e9ecef;
    margin: 2rem 0;
}

/* Expander Styling */
[data-testid="stExpander"] {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 10px;
    margin-bottom: 0.75rem;
    transition: all 0.2s ease;
}

[data-testid="stExpander"]:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border-color: #6366f1;
}

/* Spinner Customization */
.stSpinner > div {
    border-top-color: #6366f1 !important;
}

/* ============================================
   DARK THEME (System Preference)
   ============================================ */
@media (prefers-color-scheme: dark) {
    .stApp, body, .reportview-container, .main {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%) !important;
        color: #e6edf3 !important;
    }
    
    /* Sidebar - Dark */
    section[data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        background: #161b22 !important;
        color: #e6edf3 !important;
        border-right: 1px solid #30363d;
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton button, 
    [data-testid="stSidebar"] .stRadio,
    [data-testid="stSidebar"] label {
        color: #c9d1d9 !important;
    }
    
    /* Input Fields - Dark */
    .stTextArea textarea, .stTextInput input {
        background: #0d1117 !important;
        color: #e6edf3 !important;
        border: 2px solid #30363d;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 4px rgba(129, 140, 248, 0.2);
    }
    
    /* Headings - Dark */
    h1, h2, h3, .stSubheader, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f0f6fc !important;
        text-shadow: 0 2px 16px rgba(129, 140, 248, 0.25);
    }
    
    /* Buttons - Dark */
    .stButton button {
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%) !important;
        box-shadow: 0 4px 12px rgba(129, 140, 248, 0.4);
    }
    
    .stButton button:hover {
        box-shadow: 0 8px 24px rgba(129, 140, 248, 0.5) !important;
    }
    
    /* File Uploader - Dark */
    [data-testid="stFileUploader"] {
        background: #0d1117;
        border-color: #30363d;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #818cf8;
        background: #1c2128;
    }
    
    /* Status Messages - Dark */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        color: #34d399 !important;
        border-left-color: #34d399;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        color: #f87171 !important;
        border-left-color: #f87171;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        color: #60a5fa !important;
        border-left-color: #60a5fa;
    }
    
    /* Dividers - Dark */
    hr {
        border-top: 1px solid #30363d;
    }
    
    /* Expander - Dark */
    [data-testid="stExpander"] {
        background: #0d1117;
        border: 1px solid #30363d;
    }
    
    [data-testid="stExpander"]:hover {
        box-shadow: 0 4px 12px rgba(129, 140, 248, 0.15);
        border-color: #818cf8;
    }
}

/* ============================================
   MOBILE RESPONSIVE
   ============================================ */
@media screen and (max-width: 768px) {
    .stApp {
        padding: 4vw !important;
    }
    
    [data-testid="block-container"] {
        padding-top: 1rem !important;
    }
    
    h1 { font-size: 1.75rem !important; }
    h2 { font-size: 1.35rem !important; }
    
    .stButton button {
        font-size: 0.95rem !important;
        padding: 10px 24px !important;
        width: 100%;
    }
    
    .stTextArea textarea, .stTextInput input {
        font-size: 0.95rem !important;
        padding: 12px 14px !important;
    }
    
    [data-testid="column"] {
        width: 100% !important;
        margin-bottom: 1.5rem;
    }
}

/* Hide Streamlit Branding */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
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
st.sidebar.title("Dashboard")
st.sidebar.markdown("---")

# Input Method Selection
option = st.sidebar.radio(
    "Input Method",
    ("Upload File", "Paste Text"),
    help="Select how you'd like to provide your meeting transcript"
)

# History Section in Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Summary History")

if st.session_state['summary_history']:
    for idx, item in enumerate(reversed(st.session_state['summary_history'])):
        with st.sidebar.expander(f"{item['timestamp']}", expanded=False):
            st.markdown("**Transcript Preview**")
            st.text(item['transcript'][:100] + "...")
            st.markdown("**Summary**")
            st.info(item['summary'])
else:
    st.sidebar.info("No summaries generated yet")

# Clear History Button
if st.session_state['summary_history']:
    if st.sidebar.button("Clear History", use_container_width=True):
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
            placeholder="Paste your meeting transcript here...\n\nExample:\nJohn: Let's discuss Q4 goals.\nSarah: I agree, we should focus on customer retention.",
            label_visibility="collapsed",
            key="transcript_input"
        )

with col2:
    st.info("""
    **How to Use**
    
    1. Choose your input method from the sidebar
    2. Upload a file or paste your transcript
    3. Click "Generate Summary" to get AI-powered insights
    4. View previous summaries in the History section
    
    **Tips**
    
    • Include speaker names for better context
    
    • Longer transcripts yield more detailed summaries
    
    • Works with any meeting format
    """)

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
        
        # Manual Submit Button
        if st.button("Generate Summary", use_container_width=True, key="generate_btn"):
            with st.spinner("Analyzing transcript and generating summary..."):
                try:
                    summary = call_cerebras(
                        f"Summarize this meeting transcript concisely, highlighting key points and action items:\n\n{transcript}", 
                        max_tokens=300
                    )
                    
                    # Save to history
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
    <p style='margin: 0.2rem 0;'>Crafted with 💗 by P Charmi Reddy</p>
</div>
""", unsafe_allow_html=True)
