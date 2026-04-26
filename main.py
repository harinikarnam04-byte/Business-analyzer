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

# --- SESSION STATE (The "Restart" Protection) ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'final_report' not in st.session_state: 
    st.session_state.final_report = {"p1": "", "p2": "", "p3": "", "loc": "", "idea": ""}

# --- HEADER & TAGLINE ---
st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#3b82f6; font-weight:bold; font-size:1.2em;">Let’s connect to the business world</p>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('### 🔍 Audit Parameters')
    user_idea = st.text_input("Venture Idea", placeholder="e.g. Organic Cafe")
    user_loc = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    user_target = st.text_input("Target Audience", placeholder="e.g. IT Professionals")
    user_budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    user_industry = st.selectbox("Industry", ["Retail", "Service", "Food", "Tech", "Manufacturing"])
    analyze_btn = st.button("🔍 GENERATE FULL AUDIT")

if analyze_btn:
    st.session_state.page = 1
    st.session_state.final_report["loc"] = user_loc
    st.session_state.final_report["idea"] = user_idea
    with st.spinner(f"🕵️ Senior Auditor analyzing {user_loc} market..."):
        # Explicit Location-Intelligence Prompt
        audit_query = f"""
        ACT AS: Senior Business Auditor. 
        TASK: Brutal Feasibility Audit for {user_idea} in {user_loc} targeting {user_target} with ₹{user_budget}.
        
        LOCATION INTELLIGENCE:
        1. Explicitly state if {user_loc} is Tier 1, 2, or 3.
        2. Provide local-specific monthly rent and staff salary estimates for {user_loc}.
        3. Identify 3 specific types of local competitors in that area.
        4. Include: 4Ps, SWOT, Unit Economics, Success %, and 4-Step Recovery Plan.
        
        FORMATTING: No markdown. Start sections ONLY with:
        [[S1]] (Strategy & SWOT)
        [[S2]] (Economics & Location Costs)
        [[S3]] (Final Verdict & Recovery)
        """
        
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": audit_query}]
        )
        full_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # --- DATA EXTRACTION (Fixes the "Same Content" issue) ---
        try:
            st.session_state.final_report["p1"] = full_text.split("[[S1]]")[-1].split("[[S2]]")[0].strip()
            st.session_state.final_report["p2"] = full_text.split("[[S2]]")[-1].split("[[S3]]")[0].strip()
            st.session_state.final_report["p3"] = full_text.split("[[S3]]")[-1].strip()
        except:
            st.session_state.final_report["p1"] = "Sync error. Please refine location and try again."

# --- NAVIGATION ---
report = st.session_state.final_report
if report["p1"]:
    if st.session_state.page == 1:
        st.markdown(f"## 📊 Page 1: Strategic Intelligence ({report['loc']})")
        st.markdown(f'<div class="report-box">{report["p1"]}</div>', unsafe_allow_html=True)
        st.button("Next: Economics ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown(f"## 💹 Page 2: Financial Projections ({report['loc']})")
        # Visual breakdown
        pie_df = pd.DataFrame({"Category": ["Infrastructure", "Operations", "Marketing", "Reserve"], 
                               "Amt": [user_budget*0.4, user_budget*0.3, user_budget*0.2, user_budget*0.1]})
        st.plotly_chart(px.pie(pie_df, values='Amt', names='Category', hole=0.4).update_layout(
            paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), margin=dict(t=20, b=20, l=0, r=0)
        ), use_container_width=True)
        
        st.markdown(f'<div class="report-box">{report["p2"]}</div>', unsafe_allow_html=True)
        st.table(pie_df)
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif st.session_state.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{report["p3"]}</div>', unsafe_allow_html=True)
        
        # PDF/Text Download Functionality
        full_download = f"BIZVENTURE PRO AUDIT\nIdea: {report['idea']}\nLocation: {report['loc']}\n\nSTRATEGY:\n{report['p1']}\n\nECONOMICS:\n{report['p2']}\n\nVERDICT:\n{report['p3']}"
        st.download_button("📥 Download Full Audit Report", data=full_download, file_name=f"Audit_{report['idea']}.txt")
        st.button("⬅️ Back to Financials", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 Ready to connect you to the business world. Enter your parameters in the sidebar.</div>', unsafe_allow_html=True)
