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
if 'audit' not in st.session_state: 
    st.session_state.audit = {"s1": "", "s2": "", "s3": "", "loc": ""}

st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('### 🔍 Audit Parameters')
    idea = st.text_input("Venture Idea", placeholder="e.g. Beauty Parlour")
    loc = st.text_input("Location", placeholder="e.g. Hospet, Karnataka")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Service", "Food", "Tech", "Manufacturing"])
    analyze = st.button("🔍 GENERATE FULL AUDIT")

if analyze:
    st.session_state.page = 1
    st.session_state.audit["loc"] = loc
    with st.spinner(f"🕵️ Senior Auditor analyzing {loc}..."):
        # The prompt is hard-coded to require specific location intelligence
        query = f"""
        ACT AS: Senior Business Auditor. 
        TASK: Brutal Audit for {idea} in {loc} with ₹{budget}.
        
        MANDATORY INTELLIGENCE:
        1. Categorize {loc} (Tier 1, 2, or 3).
        2. Give real rent/labor costs for {loc}.
        3. Identify specific local competition in {loc}.
        4. Include all: 4Ps, SWOT, Unit Economics, 4-step loss recovery, and Success %.
        
        STRICT FORMAT: No markdown. No intro. 
        Use these exact markers:
        [[S1]]
        [[S2]]
        [[S3]]
        """
        
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": query}]
        )
        raw = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # --- BULLETPROOF SPLIT LOGIC ---
        # Splitting at [[S1]] and [[S2]] and [[S3]] ensures NO content is lost
        try:
            st.session_state.audit["s1"] = raw.split("[[S1]]")[-1].split("[[S2]]")[0].strip()
            st.session_state.audit["s2"] = raw.split("[[S2]]")[-1].split("[[S3]]")[0].strip()
            st.session_state.audit["s3"] = raw.split("[[S3]]")[-1].strip()
        except:
            st.session_state.audit["s1"] = "Syncing Error. Please try again."

# --- NAVIGATION ---
report = st.session_state.audit
current_loc = report["loc"]

if report["s1"]:
    if st.session_state.page == 1:
        st.markdown(f"## 📊 Page 1: Strategic Intelligence ({current_loc})")
        st.markdown(f'<div class="report-box">{report["s1"]}</div>', unsafe_allow_html=True)
        st.button("Next: Economics ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown(f"## 💹 Page 2: Financial Projections ({current_loc})")
        df = pd.DataFrame({"Category": ["Setup", "Operations", "Marketing", "Emergency"], 
                           "Amount": [budget*0.4, budget*0.3, budget*0.2, budget*0.1]})
        st.plotly_chart(px.pie(df, values='Amount', names='Category', hole=0.4).update_layout(
            paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), margin=dict(t=0, b=0, l=0, r=0)
        ), use_container_width=True)
        st.markdown(f'<div class="report-box">{report["s2"]}</div>', unsafe_allow_html=True)
        st.table(df)
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif st.session_state.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{report["s3"]}</div>', unsafe_allow_html=True)
        full_audit = f"BIZVENTURE AUDIT: {idea}\n\nSTRATEGY:\n{report['s1']}\n\nECONOMICS:\n{report['s2']}\n\nVERDICT:\n{report['s3']}"
        st.download_button("📥 Download Audit", data=full_audit, file_name=f"{idea}_Audit.txt")
        st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 Auditor Online. Local Intelligence Synced.</div>', unsafe_allow_html=True)
    
