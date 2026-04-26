import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
from datetime import datetime

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="wide")

# --- THEME & VISIBILITY SECURE CSS (LOCKED) ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    
    section[data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        border-right: 3px solid #2563eb; 
    }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    /* REPORT BOX: Solid White / Black Text for 100% Phone Contrast */
    .report-box { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        padding: 35px; 
        border-radius: 15px;
        border: 5px solid #2563eb;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .report-box * { color: #000000 !important; font-weight: 600 !important; line-height: 1.8; }
    
    /* TABLE FIX: Force visibility */
    .stTable, [data-testid="stTable"], [data-testid="stTable"] td { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        font-weight: 700 !important;
    }
    .legendtext { fill: #ffffff !important; font-weight: bold; }

    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }
    
    .stButton>button { 
        background-color: #2563eb !important; 
        color: #ffffff !important; 
        font-weight: 800; 
        height: 4em; 
        border-radius: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report_p1' not in st.session_state: st.session_state.report_p1 = ""
if 'report_p2' not in st.session_state: st.session_state.report_p2 = ""
if 'report_p3' not in st.session_state: st.session_state.report_p3 = ""

st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#3b82f6; font-style:italic; font-size:1.2rem;">Connecting your vision to the global business world.</p>', unsafe_allow_html=True)

# --- SIDEBAR (UNTOUCHED FUNCTIONALITY) ---
with st.sidebar:
    st.markdown('### 🔍 Venture Parameters')
    idea = st.text_input("Venture Idea", placeholder="e.g. Pet Spa")
    location = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. Pet Lovers")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    
    analyze = st.button("🔍 GENERATE FULL AUDIT")

if analyze:
    st.session_state.page = 1
    with st.spinner("🕵️ Internal Auditor: Checking spelling and local market data..."):
        prompt = f"""
        ROLE: Senior Business Auditor & Professional Copy Editor.
        TASK: Create a professional 3-part business analysis for {idea} specifically for {location}.
        STRICT RULES: ZERO spelling mistakes. NO generic advice. Deep-dive into {location} market dynamics.
        
        PART 1: 
        - GLOBAL BUSINESS TAGLINE: A catchy slogan connecting to the global world.
        - EXECUTIVE SUMMARY: Specific to the {location} landscape.
        - THE 4Ps (Product, Price, Place, Promotion).
        - SWOT ANALYSIS.
        - ENTREPRENEURIAL EXAMPLE: Relevant leader comparison.
        - FUNDING OPTIONS: Specific paths for ₹{budget}.
        - COMPETITORS ANALYSIS: Specific local competitors in {location} vs Global benchmarks.

        PART 2:
        - EXPLANATION OF EXPENDITURE.
        - CASH REQUIREMENT: Operational runway details.
        - TIME PERIOD TO SUCCESS: Realistic break-even timeline.
        - PROFIT & SALES PROJECTIONS: Be honest, conservative, and realistic.
        - UNIT ECONOMICS: Clear breakdown of margins per unit/customer.

        PART 3:
        - OUR SUGGESTION: Success Rate Percentage.
        - FINAL GO/NO-GO VERDICT.
        - LOSS RECOVERY PLAN: 4 detailed recovery steps.
        - ALTERNATIVE STARTING STRATEGY: If current plan is risky, when/where else to start?
        - REASONING FOR ANALYSIS.
        """
        resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
        full_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # Structure splitting logic
        sections = full_text.split("PART")
        st.session_state.report_p1 = sections[1] if len(sections) > 1 else full_text
        st.session_state.report_p2 = sections[2] if len(sections) > 2 else ""
        st.session_state.report_p3 = sections[3] if len(sections) > 3 else ""

# --- PAGE NAVIGATION ---
if st.session_state.report_p1:
    if st.session_state.page == 1:
        st.markdown("## 📊 Page 1: Strategic Intelligence")
        st.markdown(f'<div class="report-box">{st.session_state.report_p1}</div>', unsafe_allow_html=True)
        st.button("Next: Economics & Projections ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown("## 💹 Page 2: Financials & Unit Economics")
        df = pd.DataFrame({"Category": ["Infrastructure", "Ops & Staff", "Marketing", "Emergency Fund"], "Amount": [budget
