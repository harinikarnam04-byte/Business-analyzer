import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="centered")

# --- LIGHT YELLOW & HIGH CONTRAST UI ---
st.markdown("""
    <style>
    /* Background: Lightest Pale Yellow */
    .stApp { background-color: #fefce8; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #fef3c7 !important; border-right: 1px solid #fde68a; }
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] .stMarkdown p { color: #1e293b !important; font-weight: bold; }
    
    /* Report & Metric Boxes: Navy Background with Brightest White Text */
    .report-box, [data-testid="stMetric"] { 
        background-color: #1e293b !important; 
        color: #ffffff !important; 
        padding: 30px; 
        border-radius: 15px;
        border: 2px solid #ffffff;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    /* Force metrics and report text to be bright white */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #ffffff !important; font-weight: 800; }
    .report-box div, .report-box p, .report-box span, .report-box li { color: #ffffff !important; font-family: 'Arial', sans-serif; }

    /* Button Styling: White with Dark Border */
    .stButton>button {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 2px solid #1e293b !important;
        border-radius: 12px;
        font-weight: 800;
        width: 100%;
        height: 3.5em;
        transition: 0.3s ease;
    }
    .stButton>button:hover { background-color: #1e293b !important; color: #ffffff !important; border: 2px solid #ffffff !important; }

    .main-title { color: #1e293b !important; font-size: 3rem; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .tagline { color: #4b5563 !important; font-size: 1.2rem; text-align: center; margin-bottom: 30px; font-weight: 500; }
    
    /* Table Styling */
    .stTable { background-color: #ffffff; border-radius: 10px; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

st.markdown('<div class="main-title">BizVenture</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Entrepreneurship & Innovation Process</div>', unsafe_allow_html=True)

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.markdown('### 🛠 Settings')
    # Instant re-run on change
    lang = st.radio("Language / भाषा", ["English", "हिंदी"], key="lang_instant_update")
    st.markdown("---")
    
    idea = st.text_input("Venture Idea", placeholder="e.g. Organic Cafe")
    location = st.text_input("Location", placeholder="e.g. Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. Professionals")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    stage = st.selectbox("Venture Stage", ["MVP/Testing", "Market Entry", "Scaling"])
    
    if st.button("🚀 GENERATE PLAN"):
        st.session_state.page = 1
        with st.spinner("Preparing Professional Document..."):
            prompt = f"""
            SYSTEM: Professional Business Advisor. 
            RULES: 
            1. Perfect spelling. 
            2. NO symbols like *, #, or bolding markers. Use plain text headers and spacing.
            3. No academic labels like 'MBA' or 'Sultanpete'.
            4. Respond in {lang}.

            CONTENT:
            - Executive Strategy (SWOT and 4Ps for {target}).
            - Growth Plan (Success Rate %, ROI Timeline, Funding).
            - Financials (Year 2 and Year 3 Projected Profits & Expenses).
            - Risk & Recovery (Detailed plan to regain market share after a loss).
            - 30-second Investor Pitch.
            """
            resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
            # Logic scrub for clean output
            st.session_state.report = resp.choices[0].message.content.replace("*", "").replace("#", "")

# --- PAGE 1: STRATEGY ---
if st.session_state.page == 1:
    if st.session_state.report:
        st.markdown("### Step 1: Strategic Discovery")
        c1, c2, c3 = st.columns(3)
        c1.metric("Capital", f"₹{budget:,}")
        c2.metric("Industry", industry)
        c3.metric("Stage", stage)
        
        # Displaying first half
        content = st.session_state.report
        st.markdown(f'<div class="report-box">{content[:len(content)//2]}...</div>', unsafe_allow_html=True)
        st.button("Next: Financial Dashboard ➡️", on_click=lambda: st.session_state.update({"page": 2}))
    else:
        st.info("Fill the sidebar and click 'Generate Plan'.")

# --- PAGE 2: FINANCIALS ---
elif st.session_state.page == 2:
    st.markdown("### Step 2: Capital Allocation")
    alloc_map = {"Retail": [0.4, 0.25, 0.2, 0.15], "Tech": [0.2, 0.2, 0.5, 0.1], 
                 "Manufacturing": [0.6, 0.2, 0.1, 0.1], "Food & Beverage": [0.45, 0.25, 0.2, 0.1], 
                 "Service": [0.2, 0.3, 0.3, 0.2]}
    vals = alloc_map.get(industry, [0.25, 0.25, 0.25, 0.25])
    df = pd.DataFrame({"Category": ["Setup", "Operations", "Marketing", "Reserve"], "Amount": [budget*v for v in vals]})
    
    # Pie Chart with Mobile Legend Fix
