import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

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
        border: 4px solid #2563eb;
        margin-bottom: 20px;
    }
    .report-box * { color: #000000 !important; font-weight: 600 !important; line-height: 1.6; }
    .stTable, [data-testid="stTable"] td { background-color: #ffffff !important; color: #000000 !important; }
    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }
    .stButton>button { 
        background-color: #2563eb !important; 
        color: #ffffff !important; 
        font-weight: 800; 
        width: 100%;
        border-radius: 10px; 
        height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INDEPENDENT DATA BUFFERS (Fixes "Same Content" & "Restart" issues) ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'p1_store' not in st.session_state: st.session_state.p1_store = ""
if 'p2_store' not in st.session_state: st.session_state.p2_store = ""
if 'p3_store' not in st.session_state: st.session_state.p3_store = ""
if 'user_loc' not in st.session_state: st.session_state.user_loc = ""
if 'user_idea' not in st.session_state: st.session_state.user_idea = ""

# --- HEADER & TAGLINE ---
st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#3b82f6; font-weight:bold; font-size:1.2em;">Let’s connect to the business world</p>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('### 🔍 Audit Parameters')
    idea_in = st.text_input("Venture Idea", placeholder="e.g. Pet Grooming")
    loc_in = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    target_in = st.text_input("Target Audience", placeholder="e.g. Pet Owners")
    budget_in = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry_in = st.selectbox("Industry", ["Retail", "Service", "Food", "Tech", "Manufacturing"])
    trigger = st.button("🔍 GENERATE FULL AUDIT")

if trigger:
    st.session_state.page = 1
    st.session_state.user_loc = loc_in
    st.session_state.user_idea = idea_in
    with st.spinner(f"🕵️ Senior Auditor analyzing {loc_in}..."):
        # The prompt is hard-coded to deliver unique data per page
        full_query = f"""
        ACT AS: Senior Business Auditor. 
        TASK: Deep Audit for {idea_in} in {loc_in} for {target_in} with ₹{budget_in}.
        
        STRICT DATA ASSIGNMENT:
        
        [[PAGE_1]]:
        - City Tier (1, 2, or 3) for {loc_in}.
        - Professional Elevator Pitch & Entrepreneur Profile needed.
        - Deep Competitor Analysis for {loc_in}.
        - Funding Sources for ₹{budget_in}.
        - 4Ps & SWOT Analysis.
        
        [[PAGE_2]]:
        - Local Rent & Salary estimates specific to {loc_in}.
        - Unit Economics & Break-even month projection.
        
        [[PAGE_3]]:
        - Success % and Go/No-Go Verdict.
        - 4-Step Loss Recovery Strategy.
        
        FORMAT: No markdown. No intro. Start each part ONLY with [[PAGE_1]], [[PAGE_2]], [[PAGE_3]].
        """
        
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": full_query}]
        )
        clean_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # --- HARD ROUTING TO UNIQUE SLOTS ---
        st.session_state.p1_store = clean_text.split("[[PAGE_1]]")[-1].split("[[PAGE_2]]")[0].strip()
        st.session_state.p2_store = clean_text.split("[[PAGE_2]]")[-1].split("[[PAGE_3]]")[0].strip()
        st.session_state.p3_store = clean_text.split("[[PAGE_3]]")[-1].strip()

# --- DISPLAY ENGINE ---
report = st.session_state
if report.p1_store:
    if report.page == 1:
        st.markdown(f"## 📊 Page 1: Strategy & Setup ({report.user_loc})")
        st.markdown(f'<div class="report-box">{report.p1_store}</div>', unsafe_allow_html=True)
        st.button("Next: Economics ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif report.page == 2:
        st.markdown(f"## 💹 Page 2: Financials & Local Costs ({report.user_loc})")
        pie_df = pd.DataFrame({"Item": ["Setup", "Operations", "Marketing", "Reserve"], "Amt": [budget_in*0.4, budget_in*0.3, budget_in*0.2, budget_in*0.1]})
        st.plotly_chart(px.pie(pie_df, values='Amt', names='Item', hole=0.4).update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white")), use_container_width=True)
        st.markdown(f'<div class="report-box">{report.p2_store}</div>', unsafe_allow_html=True)
        st.table(pie_df)
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif report.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{report.p3_store}</div>', unsafe_allow_html=True)
        
        # Download Data
        final_txt = f"AUDIT: {report.user_idea}\n\nSTRATEGY:\n{report.p1_store}\n\nECONOMICS:\n{report.p2_store}\n\nVERDICT:\n{report.p3_store}"
        st.download_button("📥 Download Report", data=final_txt, file_name=f"Audit_{report.user_idea}.txt")
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 Ready to connect you to the business world. Fill the sidebar and click Generate.</div>', unsafe_allow_html=True)
    
