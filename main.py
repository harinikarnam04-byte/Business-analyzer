import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="wide")

# --- VISIBILITY SECURE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    section[data-testid="stSidebar"] { background-color: #000000 !important; }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    /* FORCE BLACK TEXT ON WHITE FOR MOBILE READABILITY */
    .report-box { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        padding: 35px; 
        border-radius: 15px;
        border: 5px solid #2563eb;
    }
    .report-box * { color: #000000 !important; font-weight: 600 !important; }
    
    .tagline { 
        font-style: italic; 
        color: #2563eb !important; 
        font-size: 1.4rem !important; 
        margin-bottom: 20px;
        display: block;
    }

    .stTable, [data-testid="stTable"], [data-testid="stTable"] td { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        font-weight: 700 !important;
    }

    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }
    .stButton>button { background-color: #2563eb !important; color: #ffffff !important; font-weight: 800; height: 4em; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('### 🔍 Search Console')
    idea = st.text_input("Venture Idea", value="Pet Spa")
    location = st.text_input("Location", value="Bangalore")
    target = st.text_input("Target Audience", value="Pet Lovers")
    budget = st.number_input("Capital (₹)", value=500000)
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    stage = st.selectbox("Venture Stage", ["MVP/Testing", "Market Entry", "Scaling"])
    
    analyze = st.button("🔍 ANALYZE NOW")

if analyze:
    st.session_state.page = 1
    with st.spinner("🕵️ Auditing & Generating Professional Report..."):
        # F-string ensures all your phone inputs are used correctly
        prompt = f"""
        ROLE: Senior Business Consultant & Copy Editor.
        TASK: Create a premium business analysis for {idea} in {location}.
        STRICT RULES: 
        1. No spelling errors. Professional grammar only.
        2. Format with clean line breaks. NO symbols like (*, #).
        
        STRUCTURE:
        - IMPACTFUL TAGLINE: A catchy slogan for the venture.
        - EXECUTIVE SUMMARY: Deep dive into the mission.
        - STRATEGIC BLUEPRINT: 4Ps and SWOT analysis.
        - ENTREPRENEUR SPIRIT: Compare to a leader like Ritesh Agarwal.
        - FUNDING & ROI: How to use ₹{budget} and projected Year 2/3 profits.
        - LOSS RECOVERY PLAN: 4 clear steps to handle financial setbacks.
        """
        resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
        st.session_state.report = resp.choices[0].message.content.replace("*", "").replace("#", "")

# --- PAGES ---
if st.session_state.report:
    if st.session_state.page == 1:
        st.markdown("## 📊 Phase 1: Strategic Intelligence")
        # Split report to show Tagline and Summary first
        st.markdown(f'<div class="report-box">{st.session_state.report[:len(st.session_state.report)//2]}</div>', unsafe_allow_html=True)
        st.button("View Financials ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown("## 💹 Phase 2: Capital & Projections")
        df = pd.DataFrame({"Category": ["Setup", "Operations", "Marketing", "Reserve"], "Amount": [budget*0.4, budget*0.25, budget*0.2, budget*0.15]})
        fig = px.pie(df, values='Amount', names='Category', hole=0.5)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### Allocation Detail (Force-Visible)")
        st.table(df)
        
        st.button("View Final Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))

    elif st.session_state.page == 3:
        st.markdown("## 🏆 Phase 3: Risk & Recovery")
        st.markdown(f'<div class="report-box">{st.session_state.report[len(st.session_state.report)//2:]}</div>', unsafe_allow_html=True)
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 Welcome. Enter details in the sidebar and click 🔍 ANALYZE NOW for your full report.</div>', unsafe_allow_html=True)
   
