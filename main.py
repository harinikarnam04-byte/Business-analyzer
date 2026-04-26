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

# --- INDEPENDENT DATA BUFFERS ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'p1_data' not in st.session_state: st.session_state.p1_data = ""
if 'p2_data' not in st.session_state: st.session_state.p2_data = ""
if 'p3_data' not in st.session_state: st.session_state.p3_data = ""
if 'loc_tag' not in st.session_state: st.session_state.loc_tag = ""
if 'idea_tag' not in st.session_state: st.session_state.idea_tag = ""

# --- HEADER & TAGLINE ---
st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#3b82f6; font-weight:bold; font-size:1.2em;">Let’s connect to the business world</p>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('### 🔍 Audit Parameters')
    in_idea = st.text_input("Venture Idea", placeholder="e.g. Luxury Spa")
    in_loc = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    in_target = st.text_input("Target Audience", placeholder="e.g. High-net-worth individuals")
    in_budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    in_indus = st.selectbox("Industry", ["Retail", "Service", "Food", "Tech", "Manufacturing"])
    go_btn = st.button("🔍 GENERATE FULL AUDIT")

if go_btn:
    st.session_state.page = 1
    st.session_state.loc_tag = in_loc
    st.session_state.idea_tag = in_idea
    with st.spinner(f"🕵️ Senior Auditor analyzing {in_loc} market dynamics..."):
        # The prompt is now re-engineered to force high-quality analysis
        deep_query = f"""
        ACT AS: Senior Business Auditor. 
        TASK: Conduct a Brutal & High-Fidelity Professional Audit for {in_idea} in {in_loc} targeting {in_target} with ₹{in_budget}.
        
        [[PAGE_1_REQUIREMENTS]]:
        - Identify City Tier (1, 2, or 3) for {in_loc}.
        - Professional Elevator Pitch & Required Entrepreneurial Profile.
        - DEEP COMPETITOR ANALYSIS: Conduct a critical analysis of current rivals in {in_loc}. Identify their service gaps, pricing weaknesses, and market saturations.
        - Specific Funding Sources (MSME, Angel, or Bootstrapping) for ₹{in_budget}.
        - Comprehensive 4Ps & SWOT Analysis.
        
        [[PAGE_2_REQUIREMENTS]]:
        - LOCALIZED FINANCIALS: Estimated monthly Rent, Labor, and Utilities specifically for {in_loc}.
        - Unit Economics: Margin per customer analysis and operational efficiency.
        - Logical Break-even month projection with a breakdown of Fixed vs Variable costs.
        
        [[PAGE_3_REQUIREMENTS]]:
        - Success percentage: XX% (Provide a definitive percentage based on market research, competitor analysis, and financial projections).
        - Go/No-Go Verdict: [DECISION] (Provide high-quality justification subject to refinement of financial projections and risk mitigation).
        - 4-Step Loss Recovery Strategy: 
          Step 1: Review and refine financial projections; identify immediate cost reduction areas.
          Step 2: Pivot customer acquisition and enhance brand visibility through targeted marketing.
          Step 3: Evaluate and adjust services/pricing to suit the current {in_loc} market demand.
          Step 4: Diversify revenue streams through strategic partnerships, events, or franchise expansion.
        
        FORMAT: NO MARKDOWN. NO INTRO. Start each page ONLY with [[PAGE_1]], [[PAGE_2]], [[PAGE_3]].
        """
        
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": deep_query}]
        )
        raw_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # --- DATA ROUTING ENGINE ---
        st.session_state.p1_data = raw_text.split("[[PAGE_1]]")[-1].split("[[PAGE_2]]")[0].strip()
        st.session_state.p2_data = raw_text.split("[[PAGE_2]]")[-1].split("[[PAGE_3]]")[0].strip()
        st.session_state.p3_data = raw_text.split("[[PAGE_3]]")[-1].strip()

# --- DISPLAY ENGINE ---
st_data = st.session_state
if st_data.p1_data:
    if st_data.page == 1:
        st.markdown(f"## 📊 Page 1: Strategy & Setup ({st_data.loc_tag})")
        st.markdown(f'<div class="report-box">{st_data.p1_data}</div>', unsafe_allow_html=True)
        st.button("Next: Economics ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st_data.page == 2:
        st.markdown(f"## 💹 Page 2: Financials & Local Costs ({st_data.loc_tag})")
        df = pd.DataFrame({"Category": ["Setup", "Operations", "Marketing", "Reserve"], "Amount": [in_budget*0.4, in_budget*0.3, in_budget*0.2, in_budget*0.1]})
        st.plotly_chart(px.pie(df, values='Amount', names='Category', hole=0.4).update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white")), use_container_width=True)
        st.markdown(f'<div class="report-box">{st_data.p2_data}</div>', unsafe_allow_html=True)
        st.table(df)
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif st_data.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{st_data.p3_data}</div>', unsafe_allow_html=True)
        
        # Download Logic
        full_audit = f"BIZVENTURE AUDIT: {st_data.idea_tag}\n\nSTRATEGY:\n{st_data.p1_data}\n\nECONOMICS:\n{st_data.p2_data}\n\nVERDICT:\n{st_data.p3_data}"
        st.download_button("📥 Download Full Audit Report", data=full_audit, file_name=f"Audit_{st_data.idea_tag}.txt")
        st.button("⬅️ Back to Financials", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 Auditor Online. Ready to connect you to the business world.</div>', unsafe_allow_html=True)
