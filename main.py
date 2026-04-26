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

    /* REPORT BOX: Solid White / Black Text for 100% Phone Contrast */
    .report-box { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        padding: 35px; 
        border-radius: 15px;
        border: 5px solid #2563eb;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .report-box * { color: #000000 !important; font-weight: 600 !important; line-height: 1.8; }
    
    /* TABLE & CHART LEGEND VISIBILITY */
    .stTable, [data-testid="stTable"], [data-testid="stTable"] td { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        font-weight: 700 !important;
    }
    .legendtext { fill: #ffffff !important; font-weight: bold; }

    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }
    
    .stButton>button { 
        background-color: #2563eb !important; 
        color: #ffffff !important; 
        font-weight: 800; 
        height: 4em; 
        border-radius: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 1
for p in ['report_p1', 'report_p2', 'report_p3']:
    if p not in st.session_state: st.session_state[p] = ""

st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#3b82f6; font-style:italic; font-size:1.1rem;">Connecting your vision to the global business world.</p>', unsafe_allow_html=True)

# --- SIDEBAR: PARAMETERS ---
with st.sidebar:
    st.markdown('### 🔍 Venture Parameters')
    idea = st.text_input("Venture Idea", placeholder="e.g. Pet Spa")
    location = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. Pet Lovers")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    
    analyze = st.button("🔍 GENERATE FULL AUDIT")

if analyze:
    st.session_state.page = 1
    with st.spinner("🕵️ Finalizing Full Audit... checking segments and spelling..."):
        prompt = f"""
        ROLE: Senior Business Auditor & Professional Copy Editor.
        TASK: Create a professional 3-part business analysis for {idea} specifically for {location}.
        STRICT RULES: ZERO spelling mistakes. NO markdown symbols (* or #). 
        YOU MUST CLEARLY LABEL EACH SECTION AS 'PART 1', 'PART 2', AND 'PART 3'.
        
        PART 1: 
        - GLOBAL BUSINESS TAGLINE.
        - EXECUTIVE SUMMARY: Specific to {location}.
        - THE 4Ps (Product, Price, Place, Promotion).
        - SWOT ANALYSIS.
        - ENTREPRENEURIAL EXAMPLE.
        - FUNDING OPTIONS (Specific for ₹{budget}).
        - COMPETITORS ANALYSIS (Local in {location} vs Global).

        PART 2:
        - EXPLANATION OF EXPENDITURE.
        - CASH REQUIREMENT & OPERATIONAL RUNWAY.
        - TIME PERIOD TO SUCCESS (Realistic break-even).
        - HONEST PROFIT & SALES PROJECTIONS: (Be conservative).
        - UNIT ECONOMICS (Margins per customer/unit).

        PART 3:
        - OUR SUGGESTION: Success Rate Percentage.
        - FINAL GO/NO-GO VERDICT.
        - LOSS RECOVERY PLAN (4 detailed steps).
        - ALTERNATIVE STARTING STRATEGY (If not suitable now, when or where else?).
        - REASONING FOR ANALYSIS.
        """
        resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
        full_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # SMART SPLITTING: Uses regex to find Part 1, 2, 3 regardless of case/format
        parts = re.split(r'PART\s*[1-3]', full_text, flags=re.IGNORECASE)
        
        # Mapping to session state
        st.session_state.report_p1 = parts[1].strip() if len(parts) > 1 else "Error: Segment 1 not found."
        st.session_state.report_p2 = parts[2].strip() if len(parts) > 2 else "Error: Segment 2 not found."
        st.session_state.report_p3 = parts[3].strip() if len(parts) > 3 else "Error: Segment 3 not found."

# --- NAVIGATION LOGIC ---
if st.session_state.report_p1:
    if st.session_state.page == 1:
        st.markdown("## 📊 Page 1: Strategic Blueprint")
        st.markdown(f'<div class="report-box">{st.session_state.report_p1}</div>', unsafe_allow_html=True)
        st.button("Next: Economics & Projections ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown("## 💹 Page 2: Financials & Unit Economics")
        df = pd.DataFrame({
            "Category": ["Infrastructure", "Ops & Staff", "Marketing", "Emergency Fund"],
            "Amount": [budget*0.4, budget*0.3, budget*0.2, budget*0.1]
        })
        fig = px.pie(df, values='Amount', names='Category', hole=0.45)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white", size=14))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f'<div class="report-box">{st.session_state.report_p2}</div>', unsafe_allow_html=True)
        st.table(df)
        
        c1, c2 = st.columns(2)
        c1.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": 1}))
        c2.button("Next: Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))

    elif st.session_state.page == 3:
        st.markdown("## 🏆 Page 3: Professional Verdict")
        st.markdown(f'<div class="report-box">{st.session_state.report_p3}</div>', unsafe_allow_html=True)
        
        # Download Export
        full_audit = f"BIZVENTURE PRO: {idea} - {location}\nGenerated: {datetime.now().strftime('%Y-%m-%d')}\n\n" + st.session_state.report_p1 + "\n\n" + st.session_state.report_p2 + "\n\n" + st.session_state.report_p3
        st.download_button(label="📥 Download Full Audit", data=full_audit, file_name=f"{idea}_Business_Audit.txt")
        
        st.button("⬅️ Back to Financials", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 System Online. Enter venture details and click 🔍 GENERATE FULL AUDIT.</div>', unsafe_allow_html=True)
