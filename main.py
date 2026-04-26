import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="wide")

# --- ULTIMATE VISIBILITY CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #000000 !important; }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    /* THE TABLE FIX: FORCE BLACK TEXT */
    .stTable, [data-testid="stTable"], [data-testid="stTable"] * { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        font-weight: 700 !important;
    }

    /* THE REPORT BOX FIX: FORCE BLACK TEXT */
    .report-box { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        padding: 30px; 
        border-radius: 10px;
        border: 4px solid #2563eb;
    }
    .report-box * { color: #000000 !important; font-weight: 600 !important; }

    /* HEADERS */
    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }

    /* BUTTONS */
    .stButton>button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 800;
        height: 4em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)

# --- SIDEBAR (USING F-STRINGS FOR PHONE CONNECTIVITY) ---
with st.sidebar:
    st.markdown('### 🔍 Search Console')
    idea = st.text_input("Venture Idea", placeholder="e.g. Smart Logistics")
    location = st.text_input("Location", placeholder="e.g. Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. Retailers")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    stage = st.selectbox("Venture Stage", ["MVP/Testing", "Market Entry", "Scaling"])
    
    analyze = st.button("🔍 ANALYZE NOW")

if analyze:
    st.session_state.page = 1
    with st.spinner("🕵️ Internal Audit & Generation..."):
        # F-string logic ensures mobile data transfer
        prompt = f"""
        ROLE: Professional Copy Editor and Business Consultant.
        TASK: Generate a business report for {idea} in {location}.
        RULES:
        1. NO spelling mistakes (Double-check 'Entrepreneur', 'Management').
        2. NO symbols like (*, #). 
        3. Include: Executive Summary, Strategy, Year 2/3 Profits, Funding for ₹{budget}, and Loss Recovery Plan.
        4. Mention a real founder (e.g., Elon Musk or Ritesh Agarwal).
        """
        resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
        st.session_state.report = resp.choices[0].message.content.replace("*", "").replace("#", "")

# --- DASHBOARD PAGES ---
if st.session_state.report:
    if st.session_state.page == 1:
        st.markdown("## 📊 Phase 1: Strategy")
        st.markdown(f'<div class="report-box">{st.session_state.report[:len(st.session_state.report)//2]}</div>', unsafe_allow_html=True)
        st.button("View Financials ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown("## 💹 Phase 2: Financials")
        df = pd.DataFrame({
            "Category": ["Setup", "Operations", "Marketing", "Reserve"],
            "Amount": [budget*0.4, budget*0.25, budget*0.2, budget*0.15]
        })
        fig = px.pie(df, values='Amount', names='Category', hole=0.5)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Allocation Details")
        st.table(df) # Forced to Black text via CSS
        
        st.button("View Risk ➡️", on_click=lambda: st.session_state.update({"page": 3}))
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))

    elif st.session_state.page == 3:
        st.markdown("## 🏆 Phase 3: Risk & Verdict")
        st.markdown(f'<div class="report-box">{st.session_state.report[len(st.session_state.report)//2:]}</div>', unsafe_allow_html=True)
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 Dashboard Ready. Click 🔍 ANALYZE NOW.</div>', unsafe_allow_html=True)
