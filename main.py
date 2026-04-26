import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="wide")

# --- FINAL HARD-CONTRAST CSS (MOBILE & DESKTOP STABLE) ---
st.markdown("""
    <style>
    /* Background: Deep Charcoal for a professional look */
    .stApp { background-color: #0f172a; }
    
    /* SIDEBAR: Solid Black - No transparency */
    section[data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        border-right: 3px solid #3b82f6; 
    }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    /* TITLES: High-Visibility White */
    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }

    /* THE REPORT BOX: SOLID WHITE WITH BLACK TEXT (Essential for Phone Visibility) */
    .report-box { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        padding: 30px; 
        border-radius: 12px;
        border: 4px solid #3b82f6;
        line-height: 1.7;
        font-size: 1.15rem;
    }
    
    /* Force all text inside the white card to remain Deep Black */
    .report-box p, .report-box li, .report-box div, .report-box span { 
        color: #000000 !important; 
        font-weight: 600 !important;
    }

    /* METRIC CARDS: Bright Blue with White Text */
    [data-testid="stMetric"] { 
        background-color: #1e40af !important; 
        border-radius: 10px;
        padding: 15px;
    }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 900 !important; }
    [data-testid="stMetricLabel"] { color: #bfdbfe !important; }

    /* ACTION BUTTON: Magnifying Glass Styled Large Blue Button */
    .stButton>button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 10px;
        font-weight: 800;
        width: 100%;
        height: 4em;
        border: none;
        font-size: 1.2rem;
    }
    
    /* Table: Force background to white for reading financial data */
    .stTable { background-color: #ffffff !important; color: #000000 !important; }
    
    /* Chart text fix */
    .legendtext { fill: #ffffff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)

# --- SIDEBAR: INPUTS POWERED BY F-STRINGS ---
with st.sidebar:
    st.markdown('### 🔍 Search Intelligence')
    idea = st.text_input("Venture Idea", placeholder="e.g. Smart Logistics")
    location = st.text_input("Location", placeholder="e.g. Jayanagar")
    target = st.text_input("Target Audience", placeholder="e.g. Retailers")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    stage = st.selectbox("Venture Stage", ["MVP/Testing", "Market Entry", "Scaling", "Maturity"])
    
    # Analyze button triggers simultaneous dashboard update
    analyze = st.button("🔍 ANALYZE NOW")

if analyze:
    st.session_state.page = 1
    with st.spinner("🔍 Auditing Spelling & Generating Report..."):
        # F-String connection ensures mobile inputs are captured correctly
        prompt = f"""
        SYSTEM: Senior Business Analyst. 
        MANDATORY: PERFORM A FULL SPELLING AUDIT. Ensure terms like 'Entrepreneur', 'Accrual', and 'Strategic' are perfect.
        FORMAT: NO symbols (*, #, _). Use Capital Headers and clear spacing only.
        
        REQUIRED CONTENT:
        1. EXECUTIVE SUMMARY
        2. STRATEGY: SWOT & 4Ps
        3. REAL-WORLD ENTREPRENEUR EXAMPLE: Mention a specific famous founder.
        4. FUNDING STRATEGY: Specific options based on ₹{budget}.
        5. GROWTH PLAN: Year 2 and Year 3 Projections.
        6. LOSS RECOVERY PLAN: Detailed steps to regain market share after a setback.
        
        INPUTS: Idea: {idea}, Location: {location}, Target: {target}, Budget: ₹{budget}, Industry: {industry}, Stage: {stage}.
        """
        resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
        # Mechanical clean-up of symbols
        st.session_state.report = resp.choices[0].message.content.replace("*", "").replace("#", "")

# --- MAIN DASHBOARD PAGES ---
if st.session_state.report:
    if st.session_state.page == 1:
        st.markdown("## 📊 Strategic Intelligence")
        c1, c2, c3 = st.columns(3)
        c1.metric("Capital", f"₹{budget:,}")
        c2.metric("Industry", industry)
        c3.metric("Phase", stage)
        
        st.markdown(f'<div class="report-box">{st.session_state.report[:len(st.session_state.report)//2]}</div>', unsafe_allow_html=True)
        st.button("View Financials ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown("## 💹 Capital Allocation")
        df = pd.DataFrame({
            "Category": ["Setup", "Operations", "Marketing", "Reserve"],
            "Amount": [budget*0.4, budget*0.25, budget*0.2, budget*0.15]
        })
        
        fig = px.pie(df, values='Amount', names='Category', hole=0.5)
        # Legend set to white to stand out against the background
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="#ffffff", size=14),
            legend=dict(orientation="h", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.table(df)
        st.button("View Risk & Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))
        st.button("⬅️ Back to Strategy", on_click=lambda: st.session_state.update({"page": 1}))

    elif st.session_state.page == 3:
        st.markdown("## 🏆 Final Verdict & Risk")
        st.markdown(f'<div class="report-box">{st.session_state.report[len(st.session_state.report)//2:]}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.download_button("📥 Save Strategy Report", st.session_state.report, file_name="Venture_Report.txt")
        st.button("⬅️ Back to Financials", on_click=lambda: st.session_state.update({"page": 2}))
else:
    # Landing message that updates as soon as inputs are analyzed
    st.markdown('<div class="report-box" style="text-align:center;">👋 Dashboard Ready. Enter venture details in the sidebar and click 🔍 ANALYZE NOW.</div>', unsafe_allow_html=True)
