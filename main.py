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

# --- INDEPENDENT MEMORY SLOTS (The "No-Repeat" Vault) ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'p1_vault' not in st.session_state: st.session_state.p1_vault = ""
if 'p2_vault' not in st.session_state: st.session_state.p2_vault = ""
if 'p3_vault' not in st.session_state: st.session_state.p3_vault = ""
if 'loc_cache' not in st.session_state: st.session_state.loc_cache = ""
if 'idea_cache' not in st.session_state: st.session_state.idea_cache = ""

# --- HEADER & TAGLINE ---
st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#3b82f6; font-weight:bold; font-size:1.2em;">Let’s connect to the business world</p>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('### 🔍 Audit Parameters')
    in_idea = st.text_input("Venture Idea", placeholder="e.g. Boutique Gym")
    in_loc = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    in_target = st.text_input("Target Audience", placeholder="e.g. Working Professionals")
    in_budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    in_indus = st.selectbox("Industry", ["Retail", "Service", "Food", "Tech", "Manufacturing"])
    generate_audit = st.button("🔍 GENERATE FULL AUDIT")

if generate_audit:
    st.session_state.page = 1
    st.session_state.loc_cache = in_loc
    st.session_state.idea_cache = in_idea
    with st.spinner(f"🕵️ Senior Auditor analyzing {in_loc}..."):
        # The prompt is now strictly segmented to prevent "leakage"
        final_query = f"""
        ACT AS: Senior Business Auditor. 
        TASK: Brutal Professional Audit for {in_idea} in {in_loc} targeting {in_target} with ₹{in_budget}.
        
        [[PAGE_1]]:
        - City Tier (1, 2, or 3) for {in_loc}.
        - Elevator Pitch.
        - Entrepreneurial Inspiration (MAX 3 LINES).
        - Deep Competitor Analysis for {in_loc} (Identify gaps and weaknesses).
        - Specific Funding Sources for ₹{in_budget}.
        - 4Ps & SWOT Analysis.
        
        [[PAGE_2]]:
        - Localized Intelligence: Specific monthly rent and salary estimates for {in_loc}.
        - Unit Economics & Monthly Expense Breakdown.
        - Logical Break-even month projection.
        
        [[PAGE_3]]:
        - Success percentage: XX% (Based on market research and competition).
        - Go/No-Go Verdict: [Decision] (Justification based on risk).
        - 4-Step Loss Recovery Strategy:
          Step 1: Financial Review & Cost Reduction.
          Step 2: Customer Acquisition Pivot.
          Step 3: Pricing & Service Adjustment.
          Step 4: Revenue Diversification.
        
        STRICT RULES: NO MARKDOWN. NO INTRO. 
        You MUST put markers [[S1]], [[S2]], and [[S3]] before each respective page content.
        """
        
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": final_query}]
        )
        raw_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # --- BULLETPROOF PARSING ---
        try:
            st.session_state.p1_vault = raw_text.split("[[S1]]")[-1].split("[[S2]]")[0].strip()
            st.session_state.p2_vault = raw_text.split("[[S2]]")[-1].split("[[S3]]")[0].strip()
            st.session_state.p3_vault = raw_text.split("[[S3]]")[-1].strip()
        except:
            st.session_state.p1_vault = "Syncing error. Please try again."

# --- NAVIGATION & DISPLAY ---
report = st.session_state
if report.p1_vault:
    if report.page == 1:
        st.markdown(f"## 📊 Page 1: Strategic Setup ({report.loc_cache})")
        st.markdown(f'<div class="report-box">{report.p1_vault}</div>', unsafe_allow_html=True)
        st.button("Next: Economics ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif report.page == 2:
        st.markdown(f"## 💹 Page 2: Financial Deep-Dive ({report.loc_cache})")
        pie_df = pd.DataFrame({"Item": ["Setup", "Ops", "Marketing", "Reserve"], "Amt": [in_budget*0.4, in_budget*0.3, in_budget*0.2, in_budget*0.1]})
        st.plotly_chart(px.pie(pie_df, values='Amt', names='Item', hole=0.4).update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white")), use_container_width=True)
        st.markdown(f'<div class="report-box">{report.p2_vault}</div>', unsafe_allow_html=True)
        st.table(pie_df)
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif report.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{report.p3_vault}</div>', unsafe_allow_html=True)
        
        full_report = f"BIZVENTURE PRO AUDIT: {report.idea_cache}\n\nSTRATEGY:\n{report.p1_vault}\n\nECONOMICS:\n{report.p2_vault}\n\nVERDICT:\n{report.p3_vault}"
        st.download_button("📥 Download Report", data=full_report, file_name=f"Audit_{report.idea_cache}.txt")
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 Auditor Online. Ready to connect you to the business world.</div>', unsafe_allow_html=True)
