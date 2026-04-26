import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px
from datetime import datetime
import re

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="wide")

# --- THEME PRESERVATION (LOCKED) ---
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
    
    /* TABLE & CHART LEGEND VISIBILITY */
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
for p in ['report_p1', 'report_p2', 'report_p3']:
    if p not in st.session_state: st.session_state[p] = ""

st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#3b82f6; font-style:italic; font-size:1.1rem;">Connecting your vision to the global business world.</p>', unsafe_allow_html=True)

# --- SIDEBAR: PARAMETERS ---
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
    with st.spinner(f"🕵️ Analyzing {location} market tier and competitor intelligence..."):
        prompt = f"""
        ROLE: High-Level Business Auditor & Market Intelligence Expert.
        TASK: Perform a brutal, honest, and location-specific feasibility audit for {idea} in {location}.
        
        INTELLIGENCE DIRECTIVES:
        1. FEASIBILITY CHECK: Determine if this business is actually possible in {location} with a budget of ₹{budget}.
        2. CITY TIER ANALYSIS: Adjust Unit Economics, Rent, and Labor for {location} (Tier 1 vs Tier 2/3). 
        3. COMPETITOR MAPPING: Identify specific saturation levels and local competitor types in {location}.
        4. ZERO spelling mistakes. NO markdown symbols (* or #). 
        5. USE HEADINGS 'PART 1', 'PART 2', AND 'PART 3'.

        PART 1: Global Tagline, Location-Specific Executive Summary, 4Ps, SWOT (Specific to {location}), Entrepreneurial Example, Funding Paths for ₹{budget}, and Detailed Competitor Analysis.
        PART 2: Realistic Expenditure (Local rent/labor), Cash Requirement, Time to Success, Conservative Sales Projections, and Location-based Unit Economics.
        PART 3: Success Rate %, Brutal Go/No-Go Verdict, 4-Step Loss Recovery Plan, Alternative Strategy, and Reasoning for Analysis.
        """
        resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
        full_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # SMART SPLITTING
        parts = re.split(r'PART\s*[1-3]', full_text, flags=re.IGNORECASE)
        st.session_state.report_p1 = parts[1].strip() if len(parts) > 1 else "Error generating Segment 1."
        st.session_state.report_p2 = parts[2].strip() if len(parts) > 2 else "Error generating Segment 2."
        st.session_state.report_p3 = parts[3].strip() if len(parts) > 3 else "Error generating Segment 3."

# --- NAVIGATION LOGIC ---
if st.session_state.report_p1:
    if st.session_state.page == 1:
        st.markdown(f"## 📊 Page 1: Strategic Intelligence for {location}")
        st.markdown(f'<div class="report-box">{st.session_state.report_p1}</div>', unsafe_allow_html=True)
        st.button("Next: Economics & Projections ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown(f"## 💹 Page 2: Financials & Unit Economics ({location})")
        df = pd.DataFrame({
            "Category": ["Setup Costs", "Ops & Staff", "Marketing", "Emergency Fund"],
            "Amount": [budget*0.4, budget*0.3, budget*0.2, budget*0.1]
        })
        st.plotly_chart(px.pie(df, values='Amount', names='Category', hole=0.45).update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white")), use_container_width=True)
        st.markdown(f'<div class="report-box">{st.session_state.report_p2}</div>', unsafe_allow_html=True)
        st.table(df)
        
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif st.session_state.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{st.session_state.report_p3}</div>', unsafe_allow_html=True)
        
        full_audit = f"BIZVENTURE PRO: {idea} - {location}\nGenerated: {datetime.now().strftime('%Y-%m-%d')}\n\n" + st.session_state.report_p1 + "\n\n" + st.session_state.report_p2 + "\n\n" + st.session_state.report_p3
        st.download_button(label="📥 Download Full Audit", data=full_audit, file_name=f"{idea}_{location}_Audit.txt")
        st.button("⬅️ Back to Financials", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 System Online. Localized intelligence active.</div>', unsafe_allow_html=True)
