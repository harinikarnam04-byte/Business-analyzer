import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="centered")

# --- HIGH-CONTRAST READABILITY THEME ---
st.markdown("""
    <style>
    /* Background: Light Cool Grey (Easy on eyes) */
    .stApp { background-color: #f1f5f9; }
    
    /* SIDEBAR: Dark for clear separation */
    section[data-testid="stSidebar"] { 
        background-color: #0f172a !important; 
        border-right: 1px solid #1e293b; 
    }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    /* REPORT BOX: Solid White with Deep Slate Black text (Perfect Contrast) */
    .report-box { 
        background-color: #ffffff !important; 
        color: #0f172a !important; 
        padding: 35px; 
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        line-height: 1.8;
        font-size: 1.1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* METRIC CARDS: Blue background with White text for visibility */
    [data-testid="stMetric"] { 
        background-color: #2563eb !important; 
        padding: 20px; 
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { 
        color: #ffffff !important; 
    }

    /* BUTTONS: Bold Blue */
    .stButton>button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 8px;
        font-weight: 700;
        width: 100%;
        height: 3.5em;
        border: none;
    }
    
    .main-title { font-size: 2.8rem; font-weight: 800; text-align: center; color: #0f172a !important; margin: 0; }
    .tagline { font-size: 1.1rem; text-align: center; color: #475569 !important; margin-bottom: 30px; }
    
    /* Clean Table */
    .stTable { background-color: #ffffff; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

st.markdown('<div class="main-title">BizVenture</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Entrepreneurial Strategy & Innovation Process</div>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('### 📋 Venture Setup')
    idea = st.text_input("Venture Idea", placeholder="e.g. Smart Logistics")
    location = st.text_input("Location", placeholder="e.g. Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. Retailers")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    stage = st.selectbox("Venture Stage", ["MVP/Testing", "Market Entry", "Scaling", "Maturity"])
    
    if st.button("🚀 GENERATE ANALYSIS"):
        st.session_state.page = 1
        with st.spinner("Processing Strategy..."):
            prompt = f"""
            SYSTEM: Professional Business Advisor. Use PERFECT spelling. 
            REMOVE ALL asterisks (*), hashtags (#), and markdown. 
            Output must be CLEAN PLAIN TEXT with professional headers.
            
            INPUT: Idea: {idea}, Location: {location}, Target: {target}, Budget: ₹{budget}, Industry: {industry}, Stage: {stage}.
            
            REQUIRED SECTIONS:
            1. Executive Summary
            2. Strategy (SWOT & 4Ps)
            3. Growth (Success %, ROI, Year 2 & 3 Profits)
            4. Loss Recovery Plan (How to regain market share after a loss)
            5. Investor Pitch
            """
            resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
            st.session_state.report = resp.choices[0].message.content.replace("*", "").replace("#", "")

# --- PAGE 1: STRATEGY ---
if st.session_state.page == 1:
    if st.session_state.report:
        st.markdown("### I. Strategic Analysis")
        c1, c2, c3 = st.columns(3)
        c1.metric("Budget", f"₹{budget:,}")
        c2.metric("Sector", industry)
        c3.metric("Stage", stage)
        
        st.markdown(f'<div class="report-box">{st.session_state.report[:len(st.session_state.report)//2]}...</div>', unsafe_allow_html=True)
        st.button("View Financials ➡️", on_click=lambda: st.session_state.update({"page": 2}))
    else:
        st.info("Fill the sidebar and click 'Generate' to see the report.")

# --- PAGE 2: FINANCIALS ---
elif st.session_state.page == 2:
    st.markdown("### II. Capital Allocation")
    alloc_map = {"Retail": [0.4, 0.25, 0.2, 0.15], "Tech": [0.2, 0.2, 0.5, 0.1], 
                 "Manufacturing": [0.6, 0.2, 0.1, 0.1], "Food & Beverage": [0.45, 0.25, 0.2, 0.1], 
                 "Service": [0.2, 0.3, 0.3, 0.2]}
    vals = alloc_map.get(industry, [0.25, 0.25, 0.25, 0.25])
    df = pd.DataFrame({"Category": ["Setup", "Operations", "Marketing", "Reserve"], "Amount": [budget*v for v in vals]})
    
    fig = px.pie(df, values='Amount', names='Category', hole=0.5, color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(legend=dict(orientation="h", y=-0.5, xanchor="center", x=0.5))
    st.plotly_chart(fig, use_container_width=True)
    st.table(df)
    
    st.button("View Risk & Pitch ➡️", on_click=lambda: st.session_state.update({"page": 3}))
    st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))

# --- PAGE 3: FINAL VERDICT ---
elif st.session_state.page == 3:
    st.markdown("### III. Projections & Risk Recovery")
    st.markdown(f'<div class="report-box">...{st.session_state.report[len(st.session_state.report)//2:]}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.download_button("📥 Download Plan (PDF Ready)", st.session_state.report, file_name="Venture_Plan.txt")
    st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 2}))
