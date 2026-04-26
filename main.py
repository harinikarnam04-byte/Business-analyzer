import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="wide")

# --- HIGH-CONTRAST "PAPER & INK" THEME ---
st.markdown("""
    <style>
    /* Background: Soft Grey */
    .stApp { background-color: #f8fafc; }
    
    /* Global Text: Deep Slate Black (Highest Readability) */
    h1, h2, h3, p, span, div, label, li { 
        color: #0f172a !important; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar: Dark Navy (Separates inputs from output) */
    section[data-testid="stSidebar"] { 
        background-color: #0f172a !important; 
    }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    /* REPORT BOX: Pure White Background + Black Text + Blue Accents */
    .report-box { 
        background-color: #ffffff !important; 
        color: #0f172a !important; 
        padding: 40px; 
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        line-height: 1.8;
        font-size: 1.15rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Metrics: Bright Blue for visibility */
    [data-testid="stMetric"] { 
        background-color: #ffffff !important; 
        border: 2px solid #2563eb;
        padding: 20px; 
        border-radius: 12px;
    }
    [data-testid="stMetricValue"] { color: #2563eb !important; font-weight: 800; }
    [data-testid="stMetricLabel"] { color: #64748b !important; }

    /* BUTTONS: Deep Blue with Magnifying Glass Feel */
    .stButton>button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 10px;
        font-weight: 700;
        width: 100%;
        height: 3.5em;
        border: none;
        font-size: 1.1rem;
    }
    
    .main-title { font-size: 3rem; font-weight: 800; text-align: center; color: #0f172a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

st.markdown('<h1 class="main-title">🔍 BizVenture</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#64748b;">Entrepreneurial Process Dashboard</p>', unsafe_allow_html=True)

# --- SIDEBAR: LIVE SEARCH CONSOLE ---
with st.sidebar:
    st.markdown('### 🔍 Search Console')
    idea = st.text_input("Venture Idea", placeholder="e.g. Smart Logistics")
    location = st.text_input("Location", placeholder="e.g. Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. Retailers")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    stage = st.selectbox("Venture Stage", ["MVP/Testing", "Market Entry", "Scaling", "Maturity"])
    
    # Generate button acts as the final trigger
    generate = st.button("🔍 ANALYZE NOW")

if generate:
    st.session_state.page = 1
    with st.spinner("🔍 Scanning Market Data..."):
        prompt = f"""
        SYSTEM: Senior Business Advisor. 
        RULES: 
        1. NO asterisks (*), hashtags (#), or symbols. 
        2. Provide REAL-WORLD Entrepreneur examples for each stage (e.g., how founders like Elon Musk or local Indian entrepreneurs did it).
        3. Use perfect English.
        
        INPUT: {idea}, {location}, {target}, ₹{budget}, {industry}, {stage}.
        
        REQUIRED SECTIONS:
        - Executive Summary
        - Strategy: SWOT & 4Ps (Include an Entrepreneur Example).
        - Funding: Best options for ₹{budget} (Bootstrapping, Angel, etc.).
        - Future: Profits/Expenses for Year 2 and Year 3.
        - Risk: Loss Recovery Plan to regain market share.
        - Investor Pitch.
        """
        resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
        st.session_state.report = resp.choices[0].message.content.replace("*", "").replace("#", "")

# --- MAIN DASHBOARD DISPLAY ---
if st.session_state.report:
    if st.session_state.page == 1:
        st.markdown("### 📊 Phase 1: Strategic Intelligence")
        c1, c2, c3 = st.columns(3)
        c1.metric("Target Capital", f"₹{budget:,}")
        c2.metric("Industry Sector", industry)
        c3.metric("Current Stage", stage)
        
        st.markdown(f'<div class="report-box">{st.session_state.report[:len(st.session_state.report)//2]}...</div>', unsafe_allow_html=True)
        st.button("View Financial Dashboard ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown("### 💹 Phase 2: Resource Allocation")
        # Dynamic Math
        allocs = [0.4, 0.25, 0.2, 0.15]
        df = pd.DataFrame({"Category": ["Setup", "Operations", "Marketing", "Reserve"], "Amount": [budget*v for v in allocs]})
        
        fig = px.pie(df, values='Amount', names='Category', hole=0.5, color_discrete_sequence=px.colors.qualitative.G10)
        fig.update_layout(legend=dict(orientation="h", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig, use_container_width=True)
        st.table(df)
        
        st.button("View Growth & Risk ➡️", on_click=lambda: st.session_state.update({"page": 3}))
        st.button("⬅️ Back to Strategy", on_click=lambda: st.session_state.update({"page": 1}))

    elif st.session_state.page == 3:
        st.markdown("### 🏆 Phase 3: The Verdict")
        st.markdown(f'<div class="report-box">...{st.session_state.report[len(st.session_state.report)//2:]}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.download_button("📥 Download PDF Ready Plan", st.session_state.report, file_name="BizVenture_Plan.txt")
        st.button("⬅️ Back to Financials", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.info("👋 Welcome! Please enter your business details in the sidebar and click the 🔍 Search button to generate your dashboard.")
