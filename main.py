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

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'p1_mem' not in st.session_state: st.session_state.p1_mem = ""
if 'p2_mem' not in st.session_state: st.session_state.p2_mem = ""
if 'p3_mem' not in st.session_state: st.session_state.p3_mem = ""
if 'loc_tag' not in st.session_state: st.session_state.loc_tag = ""

# --- HEADER & TAGLINE ---
st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#3b82f6; font-weight:bold; font-size:1.2em;">Let’s connect to the business world</p>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('### 🔍 Audit Parameters')
    u_idea = st.text_input("Venture Idea", placeholder="e.g. Organic Cafe")
    u_loc = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    u_target = st.text_input("Target Audience", placeholder="e.g. Professionals")
    u_budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    u_indus = st.selectbox("Industry", ["Retail", "Service", "Food", "Tech", "Manufacturing"])
    trigger = st.button("🔍 GENERATE FULL AUDIT")

if trigger:
    st.session_state.page = 1
    st.session_state.p1_mem = "" 
    st.session_state.loc_tag = u_loc
    
    with st.spinner(f"🕵️ Senior Auditor performing localized deep-dive for {u_loc}..."):
        # RE-ENGINEERED SMART PROMPT
        query = f"""
        ACT AS: Senior Business Auditor. 
        TASK: High-Fidelity Audit for {u_idea} in {u_loc} for {u_target} with ₹{u_budget}.
        
        GEOGRAPHIC INTELLIGENCE PROTOCOL:
        1. CLASSIFY LOCATION: Determine if {u_loc} is Tier 1 (Metro), Tier 2 (City), or Tier 3 (Town/Taluk).
        2. VERIFY MARKET REALITY: If Tier 3 (like Hosanagara), do NOT assume standard urban competition. If specialized shops do not exist there, list "Market Monopoly Potential" as a strength and "Limited Purchasing Power" as a threat.
        3. FINANCIAL ALIGNMENT: Adjust rent and operational costs based on the Tier. A Tier 3 town should have rent 70-80% lower than Bangalore.
        4. NO HALLUCINATION: If you cannot find a specific competitor in {u_loc}, describe the typical unorganized competition (e.g., small local vendors) instead of making up names[cite: 1].
        
        PART 1 (Strategic Analysis):
        - Identified City Tier & Market Profile.
        - Elevator Pitch & Inspiration.
        - Realistic Competitor Analysis (Local gaps vs. Metro saturation).
        - 4Ps & SWOT Analysis (Strictly localized to {u_loc}).
        
        PART 2 (Local Economics):
        - Tier-adjusted Rent/Salary/Ops breakdown.
        
        PART 3 (Final Verdict):
        - Success % based on local feasibility.
        - Go/No-Go Decision.
        
        FORMAT: NO MARKDOWN. Put markers: [S1], [S2], [S3].
        """
        
        try:
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=[{"role": "user", "content": query}],
                temperature=0.0 
            )
            raw_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
            
            st.session_state.p1_mem = raw_text.split("[S1]")[-1].split("[S2]")[0].strip()
            st.session_state.p2_mem = raw_text.split("[S2]")[-1].split("[S3]")[0].strip()
            st.session_state.p3_mem = raw_text.split("[S3]")[-1].strip()
            
            st.rerun()
            
        except Exception as e:
            st.session_state.p1_mem = "Sync error. Please try again."

# --- NAVIGATION ---
s_state = st.session_state
if s_state.p1_mem:
    if s_state.page == 1:
        st.markdown(f"## 📊 Page 1: Strategy & Setup ({s_state.loc_tag})")
        st.markdown(f'<div class="report-box">{s_state.p1_mem}</div>', unsafe_allow_html=True)
        st.button("Next: Economics ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif s_state.page == 2:
        st.markdown(f"## 💹 Page 2: Financial Intelligence ({s_state.loc_tag})")
        df = pd.DataFrame({"Item": ["Infrastructure", "Ops", "Marketing", "Reserve"], "Amt": [u_budget*0.4, u_budget*0.3, u_budget*0.2, u_budget*0.1]})
        st.plotly_chart(px.pie(df, values='Amt', names='Item', hole=0.4).update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white")), use_container_width=True)
        st.markdown(f'<div class="report-box">{s_state.p2_mem}</div>', unsafe_allow_html=True)
        st.table(df)
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif s_state.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{s_state.p3_mem}</div>', unsafe_allow_html=True)
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 Welcome. Senior Auditor is analyzing Tier-specific market data.</div>', unsafe_allow_html=True)
