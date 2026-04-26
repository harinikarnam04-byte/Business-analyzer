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
    with st.spinner(f"🕵️ Syncing intelligence for {location}..."):
        # The prompt forces the AI to provide the high-level data you saw on the laptop
        audit_query = f"""
        ACT AS: Senior Business Auditor. 
        TASK: Professional Audit for {idea} in {location} (Budget: ₹{budget}).
        
        GEOGRAPHIC DIRECTIVES:
        1. Categorize {location} (Tier 1, 2, or 3).
        2. Adjust rent and labor costs for {location}.
        3. Identify specific local competitors in {location}.
        
        FORMATTING: No markdown. No intro/summary.
        You MUST use these exact markers: [SECTION_1], [SECTION_2], and [SECTION_3].
        """
        
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": audit_query}]
        )
        full_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # --- HYBRID PARSER (Fixed for Phone/Laptop mismatch) ---
        # Splitting using both Bracket and Non-Bracket markers for safety
        parts = re.split(r'\[SECTION_1\]|SECTION 1|\[SECTION 1\]', full_text, flags=re.IGNORECASE)
        if len(parts) > 1:
            main_content = parts[1]
            
            # Extract Section 1
            s1_split = re.split(r'\[SECTION_2\]|SECTION 2|\[SECTION 2\]', main_content, flags=re.IGNORECASE)
            st.session_state.report_p1 = s1_split[0].strip()
            
            # Extract Section 2 and 3
            if len(s1_split) > 1:
                s2_split = re.split(r'\[SECTION_3\]|SECTION 3|\[SECTION 3\]', s1_split[1], flags=re.IGNORECASE)
                st.session_state.report_p2 = s2_split[0].strip()
                if len(s2_split) > 1:
                    st.session_state.report_p3 = s2_split[1].strip()
        
        # Fallback if parsing gets weird on mobile
        if not st.session_state.report_p1:
            st.session_state.report_p1 = "Audit Loaded. Please use navigation to view."

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
        st.markdown(f'<div class="report-box">{st.session_state.report_p2 if st.session_state.report_p2 else "Processing location data..."}</div>', unsafe_allow_html=True)
        st.table(df)
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif st.session_state.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{st.session_state.report_p3 if st.session_state.report_p3 else "Calculating final verdict..."}</div>', unsafe_allow_html=True)
        full_audit = f"BIZVENTURE AUDIT: {idea} in {location}\n\n{st.session_state.report_p1}\n\n{st.session_state.report_p2}\n\n{st.session_state.report_p3}"
        st.download_button(label="📥 Download Audit", data=full_audit, file_name=f"{idea}_Audit.txt")
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 System Online. Professional Auditor mode active.</div>', unsafe_allow_html=True)
