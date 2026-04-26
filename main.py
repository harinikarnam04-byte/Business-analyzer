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
    .report-box { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        padding: 25px; 
        border-radius: 15px;
        border: 5px solid #2563eb;
    }
    .report-box * { color: #000000 !important; font-weight: 600 !important; line-height: 1.6; }
    .stTable, [data-testid="stTable"], [data-testid="stTable"] td { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        font-weight: 700 !important;
    }
    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }
    .stButton>button { 
        background-color: #2563eb !important; 
        color: #ffffff !important; 
        font-weight: 800; 
        height: 3.5em; 
        border-radius: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
for p in ['report_p1', 'report_p2', 'report_p3']:
    if p not in st.session_state: st.session_state[p] = ""

st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('### 🔍 Parameters')
    idea = st.text_input("Venture Idea", placeholder="e.g. Beauty Parlour")
    location = st.text_input("Location", placeholder="e.g. Hospet, Karnataka")
    target = st.text_input("Target Audience", placeholder="e.g. Local Residents")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    analyze = st.button("🔍 GENERATE FULL AUDIT")

if analyze:
    st.session_state.page = 1
    with st.spinner(f"🕵️ Professional Audit: Syncing intelligence for {location}..."):
        # Explicit Auditor Prompt - No Summary allowed
        audit_query = f"""
        ACT AS: Senior Business Auditor. 
        CRITICAL: Analyze {idea} in {location} for a budget of ₹{budget}.
        
        INTELLIGENCE DIRECTIVES:
        1. DO NOT summarize first. START with [SECTION_1].
        2. CATEGORIZE {location} as Tier 1, 2, or 3.
        3. ADJUST rent/labor/utility costs specifically for {location}.
        4. MAP actual local competitor saturation in that specific area.
        5. ZERO spelling mistakes. NO markdown symbols (* or #).
        
        [SECTION_1]: Global Tagline, Location-Specific Executive Summary, 4Ps, SWOT, Entrepreneurial Example, Funding for ₹{budget}, and Local Competitor Mapping.
        [SECTION_2]: Detailed Expenditure for {location}, Cash Runway, Time to Success, Conservative Sales Projections, and Unit Economics.
        [SECTION_3]: Success Rate %, Brutal Go/No-Go Verdict, 4-Step Loss Recovery, Alternative Strategy, and Reasoning.
        """
        
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": audit_query}]
        )
        full_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # Aggressive Regex: Ignores everything except the tagged sections
        s1 = re.search(r'\[SECTION_1\](.*?)\[SECTION_2\]', full_text, re.DOTALL | re.IGNORECASE)
        s2 = re.search(r'\[SECTION_2\](.*?)\[SECTION_3\]', full_text, re.DOTALL | re.IGNORECASE)
        s3 = re.search(r'\[SECTION_3\](.*)', full_text, re.DOTALL | re.IGNORECASE)

        st.session_state.report_p1 = s1.group(1).strip() if s1 else "Error: Restart Audit."
        st.session_state.report_p2 = s2.group(1).strip() if s2 else "Error: Restart Audit."
        st.session_state.report_p3 = s3.group(1).strip() if s3 else "Error: Restart Audit."

# --- NAVIGATION ---
if st.session_state.report_p1:
    if st.session_state.page == 1:
        st.markdown(f"## 📊 Page 1: Strategic Intelligence ({location})")
        st.markdown(f'<div class="report-box">{st.session_state.report_p1}</div>', unsafe_allow_html=True)
        st.button("Next: Economics ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown(f"## 💹 Page 2: Financial Projections ({location})")
        df = pd.DataFrame({"Category": ["Setup", "Ops", "Marketing", "Reserve"], "Amount": [budget*0.4, budget*0.3, budget*0.2, budget*0.1]})
        st.plotly_chart(px.pie(df, values='Amount', names='Category', hole=0.4).update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white")), use_container_width=True)
        st.markdown(f'<div class="report-box">{st.session_state.report_p2}</div>', unsafe_allow_html=True)
        st.table(df)
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif st.session_state.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{st.session_state.report_p3}</div>', unsafe_allow_html=True)
        full_audit = f"BIZVENTURE AUDIT: {idea} in {location}\n\n{st.session_state.report_p1}\n\n{st.session_state.report_p2}\n\n{st.session_state.report_p3}"
        st.download_button(label="📥 Download Audit", data=full_audit, file_name=f"{idea}_{location}_Audit.txt")
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 System Online. Professional Auditor mode active.</div>', unsafe_allow_html=True)
