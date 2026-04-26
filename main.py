import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="centered")

# --- MODERN SLATE & EMERALD THEME ---
st.markdown("""
    <style>
    /* Background: Ghost White (Very professional, easy on eyes) */
    .stApp { background-color: #f8fafc; }
    
    /* Global Text: Dark Slate Grey */
    h1, h2, h3, p, span, div, label, li { 
        color: #334155 !important; 
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Sidebar: Muted Cool Grey */
    section[data-testid="stSidebar"] { 
        background-color: #f1f5f9 !important; 
        border-right: 1px solid #e2e8f0; 
    }
    
    /* Report & Metric Boxes: White with Emerald Accent Border */
    .report-box, [data-testid="stMetric"] { 
        background-color: #ffffff !important; 
        color: #334155 !important; 
        padding: 35px; 
        border-radius: 12px;
        border-left: 5px solid #059669; /* Emerald Green Stripe */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Metrics specifically */
    [data-testid="stMetricValue"] { color: #059669 !important; font-weight: 800; }
    [data-testid="stMetricLabel"] { color: #64748b !important; }

    /* Button Styling: Emerald Green with White Text */
    .stButton>button {
        background-color: #059669 !important;
        color: #ffffff !important;
        border-radius: 8px;
        font-weight: 700;
        width: 100%;
        height: 3.5em;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #047857 !important; 
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(5, 150, 105, 0.4);
    }

    .main-title { font-size: 3.2rem; font-weight: 800; text-align: center; color: #0f172a !important; margin-bottom: 0px; }
    .tagline { font-size: 1.1rem; text-align: center; color: #64748b !important; margin-bottom: 40px; }
    
    /* Table Styling: Professional Minimalist */
    .stTable { background-color: #ffffff; border-radius: 8px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

st.markdown('<div class="main-title">BizVenture</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Entrepreneurial Strategy & Innovation Process</div>', unsafe_allow_html=True)

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.markdown('### 📋 Venture Configuration')
    idea = st.text_input("Venture Idea", placeholder="e.g. Smart Logistics")
    location = st.text_input("Location", placeholder="e.g. Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. Retailers")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    stage = st.selectbox("Venture Stage", ["MVP/Testing", "Market Entry", "Scaling", "Maturity"])
    
    if st.button("🚀 GENERATE STRATEGY"):
        st.session_state.page = 1
        with st.spinner("Analyzing Market Dynamics..."):
            prompt = f"""
            SYSTEM: Professional Business Advisor. 
            RULES:
            1. Perfect spelling. 
            2. NO symbols like *, #, or markdown. Use plain text spacing only.
            3. English only. No academic labels like 'MBA'.
            
            INPUT: Idea: {idea}, Location: {location}, Target: {target}, Budget: ₹{budget}, Industry: {industry}, Stage: {stage}.
            
            CONTENT:
            - Executive Summary
            - Strategy: SWOT and 4Ps for {target}.
            - Financial Growth: Success Rate (%), ROI Timeline, and Funding.
            - Future Projections: Detailed Profits & Expenses for Year 2 and Year 3.
            - Risk & Recovery: Detailed Plan to regain market share after a loss.
            - 30-sec Investor Pitch.
            """
            resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
            st.session_state.report = resp.choices[0].message.content.replace("*", "").replace("#", "")

# --- PAGE 1: STRATEGY ---
if st.session_state.page == 1:
    if st.session_state.report:
        st.markdown("### I. Strategic Discovery")
        c1, c2, c3 = st.columns(3)
        c1.metric("Capital", f"₹{budget:,}")
        c2.metric("Sector", industry)
        c3.metric("Stage", stage)
        
        st.markdown(f'<div class="report-box">{st.session_state.report[:len(st.session_state.report)//2]}...</div>', unsafe_allow_html=True)
        st.button("View Financial Allocation ➡️", on_click=lambda: st.session_state.update({"page": 2}))
    else:
        st.info("Please fill the sidebar and click Generate to start your professional analysis.")

# --- PAGE 2: FINANCIAL DASHBOARD ---
elif st.session_state.page == 2:
    st.markdown("### II. Capital Allocation")
    alloc_map = {"Retail": [0.4, 0.25, 0.2, 0.15], "Tech": [0.2, 0.2, 0.5, 0.1], 
                 "Manufacturing": [0.6, 0.2, 0.1, 0.1], "Food & Beverage": [0.45, 0.25, 0.2, 0.1], 
                 "Service": [0.2, 0.3, 0.3, 0.2]}
    vals = alloc_map.get(industry, [0.25, 0.25, 0.25, 0.25])
    df = pd.DataFrame({"Category": ["Setup", "Operations", "Marketing", "Reserve"], "Amount": [budget*v for v in vals]})
    
    fig = px.pie(df, values='Amount', names='Category', hole=0.5, color_discrete_sequence=px.colors.sequential.Greens_r)
    fig.update_layout(
        showlegend=True, 
        paper_bgcolor='rgba(0,0,0,0)', 
        legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
        margin=dict(t=10, b=100, l=10, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.table(df.style.format({"Amount": "₹{:,.0f}"}))
    
    st.button("View Risk & Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))
    st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))

# --- PAGE 3: VERDICT & EXPORT ---
elif st.session_state.page == 3:
    st.markdown("### III. Projections & Risk Recovery")
    st.markdown(f'<div class="report-box">...{st.session_state.report[len(st.session_state.report)//2:]}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.download_button("📥 Save Professional Plan (PDF Ready)", st.session_state.report, file_name=f"Venture_Strategy.txt")
    st.button("⬅️ Back to Financials", on_click=lambda: st.session_state.update({"page": 2}))
