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
st.markdown('<p style="text-align:center; color:#3b82f6; font-style:italic;">Professional Market Intelligence & Audit</p>', unsafe_allow_html=True)

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
    with st.spinner(f"🕵️ Professional Audit: Factoring {location} market tier..."):
        # Unified prompt for all devices - Hard-coded Auditor Role
        audit_query = f"""
        ACT AS: Senior Business Auditor. 
        CRITICAL: Analyze {idea} in {location} for a budget of ₹{budget}.
        
        GEOGRAPHIC INTELLIGENCE (MANDATORY): 
        1. Identify if {location} is Tier 1, 2, or 3. 
        2. Adjust rent/labor costs specifically for {location} economic standards. 
        3. Map actual local competitor types and saturation in {location}.
        4. Evaluate if the venture is actually POSSIBLE/VIABLE in {location} with ₹{budget}.
        
        FORMATTING: No markdown (* or #). ZERO spelling mistakes. 
        MANDATORY TAGS: Start each section with [SECTION_1], [SECTION_2], and [SECTION_3].

        [SECTION_1]: Global Tagline, Location-Specific Executive Summary, 4Ps, SWOT, Entrepreneurial Example, Specific Funding for ₹{budget}, and Local Competitor Mapping.
        [SECTION_2]: Detailed Expenditure, Cash Runway, Time to Success (Break-even), Honest Sales Projections, and Unit Economics.
        [SECTION_3]: Success Rate %, Brutal Go/No-Go Verdict, 4-Step Loss Recovery, Alternative Strategy, and Reasoning.
        """
        
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": audit_query}]
        )
        full_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # Strict Regex Parsing for stability across all devices
        s1 = re.search(r'\[SECTION_1\](.*?)\[SECTION_2\]', full_text, re.DOTALL | re.IGNORECASE)
        s2 = re.search(r'\[SECTION_2\](.*?)\[SECTION_3\]', full_text, re.DOTALL | re.IGNORECASE)
        s3 = re.search(r'\[SECTION_3\](.*)', full_text, re.DOTALL | re.IGNORECASE)

        st.session_state.report_p1 = s1.group(1).strip() if s1 else "Analysis Error: Restart Audit."
        st.session_state.report_p2 = s2.group(1).strip() if s2 else "Analysis Error: Restart Audit."
        st.session_state.report_p3 = s3.group(1).strip() if s3 else "Analysis Error: Restart Audit."

# --- NAVIGATION ---
if st.session_state.report_p1:
    if st.session_state.page == 1:
        st
