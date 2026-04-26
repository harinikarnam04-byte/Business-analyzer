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

# --- SESSION STATE (CRITICAL FIX FOR PAGE ISSUES) ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'p1_content' not in st.session_state: st.session_state.p1_content = ""
if 'p2_content' not in st.session_state: st.session_state.p2_content = ""
if 'p3_content' not in st.session_state: st.session_state.p3_content = ""
if 'stored_loc' not in st.session_state: st.session_state.stored_loc = ""
if 'stored_idea' not in st.session_state: st.session_state.stored_idea = ""

# --- HEADER & TAGLINE ---
st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#3b82f6; font-weight:bold; font-size:1.2em;">Let’s connect to the business world</p>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('### 🔍 Audit Parameters')
    idea = st.text_input("Venture Idea", placeholder="e.g. Fashion Boutique")
    loc = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. College Students")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Service", "Food", "Tech", "Manufacturing"])
    analyze = st.button("🔍 GENERATE FULL AUDIT")

if analyze:
    st.session_state.page = 1
    st.session_state.stored_loc = loc
    st.session_state.stored_idea = idea
    with st.spinner(f"🕵️ Senior Auditor analyzing {loc} market..."):
        # The prompt is hard-locked to provide unique content for each marker
        query = f"""
        ACT AS: Senior Business Auditor. 
        TASK: Deep Audit for {idea} in {loc} for {target} with ₹{budget}.
        
        GEOGRAPHIC INTELLIGENCE:
        1. Explicitly state if {loc} is Tier 1, 2, or 3.
        2. Provide local-specific rent and labor costs for {loc}.
        3. List specific local competitors in {loc}.
        
        MANDATORY CONTENT: 4Ps, SWOT, Unit Economics, Success %, and 4-Step Recovery.
        FORMATTING: No markdown (* or #). No intro. Use markers: [[S1]], [[S2]], [[S3]].
        """
        
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": query}]
        )
        raw = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # --- UNIQUE DATA ROUTING (Fixes "Same Content" Issue) ---
        # We split the raw text and assign it to separate state variables
        st.session_state.p1_content = raw.split("[[S1]]")[-1].split("[[S2]]")[0].strip()
        st.session_state.p2_content = raw.split("[[S2]]")[-1].split("[[S3]]")[0].strip()
        st.session_state.p3_content = raw.split("[[S3]]")[-1].strip()

# --- NAVIGATION ---
if st.session_state.p1_content:
    if st.session_state.page == 1:
        st.markdown(f"## 📊 Page 1: Strategic Intelligence ({st.session_state.stored_loc})")
        st.markdown(f'<div class="report-box">{st.session_state.p1_content}</div>', unsafe_allow_html=True)
        st.button("Next: Economics ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown(f"## 💹 Page 2: Financial Projections ({st.session_state.stored_loc})")
        df = pd.DataFrame({"Category": ["Setup", "Ops", "Marketing", "Reserve"], "Amt": [budget*0.4, budget*0.3, budget*0.2, budget*0.1]})
        st.plotly_chart(px.pie(df, values='Amt', names='Category', hole=0.4).update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white")), use_container_width=True)
        st.markdown(f'<div class="report-box">{st.session_state.p2_content}</div>', unsafe_allow_html=True)
        st.table(df)
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif st.session_state.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{st.session_state.p3_content}</div>', unsafe_allow_html=True)
        
        # Download Feature
        full_txt = f"AUDIT: {st.session_state.stored_idea}\n\nSTRATEGY:\n{st.session_state.p1_content}\n\nECONOMICS:\n{st.session_state.p2_content}\n\nVERDICT:\n{st.session_state.p3_content}"
        st.download_button("📥 Download Full Audit", data=full_txt, file_name=f"Audit_{st.session_state.stored_idea}.txt")
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 Ready to audit. Enter parameters and click Generate.</div>', unsafe_allow_html=True)
