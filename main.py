import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="wide")

# --- THEME PRESERVATION: Midnight Blue & High Contrast ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    
    section[data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        border-right: 3px solid #2563eb; 
    }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    /* REPORT BOX: White Background / Black Text for Phone Readability */
    .report-box { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        padding: 35px; 
        border-radius: 15px;
        border: 5px solid #2563eb;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .report-box * { color: #000000 !important; font-weight: 600 !important; line-height: 1.8; }
    
    /* TABLE & CHART LEGEND */
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
if 'report_p1' not in st.session_state: st.session_state.report_p1 = ""
if 'report_p2' not in st.session_state: st.session_state.report_p2 = ""
if 'report_p3' not in st.session_state: st.session_state.report_p3 = ""

st.markdown('<h1 style="text-align:center;">🔍 BizVenture Pro</h1>', unsafe_allow_html=True)

# --- SIDEBAR: PARAMETERS ---
with st.sidebar:
    st.markdown('### 🔍 Venture Parameters')
    idea = st.text_input("Venture Idea", placeholder="e.g. Pet Spa")
    location = st.text_input("Location", placeholder="e.g. Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. Pet Lovers")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    
    analyze = st.button("🔍 GENERATE FULL AUDIT")

if analyze:
    st.session_state.page = 1
    with st.spinner("🕵️ Internal Spelling Audit & Quality Check in Progress..."):
        prompt = f"""
        ROLE: Senior Business Auditor & Professional Copy Editor.
        TASK: Create a professional 3-part business analysis for {idea} in {location}.
        STRICT RULES: ZERO spelling mistakes. High-quality professional language. No symbols like (*, #).
        
        PART 1: 
        - GLOBAL BUSINESS TAGLINE.
        - EXECUTIVE SUMMARY.
        - THE 4Ps (Product, Price, Place, Promotion).
        - SWOT ANALYSIS.
        - ENTREPRENEURIAL EXAMPLE (e.g. Steve Jobs, Ritesh Agarwal).
        - FUNDING OPTIONS (Paths for ₹{budget}).
        - COMPETITORS ANALYSIS (Local and Global).

        PART 2:
        - EXPLANATION OF EXPENDITURE.
        - CASH REQUIREMENT & OPERATIONAL RUNWAY.
        - TIME PERIOD TO SUCCESS (Break-even).
        - PROFIT & SALES PROJECTIONS (Be honest/conservative).
        - UNIT ECONOMICS (Margins per customer).

        PART 3:
        - OUR SUGGESTION: Success Rate Percentage.
        - FINAL GO/NO-GO VERDICT.
        - LOSS RECOVERY PLAN (4 steps).
        - ALTERNATIVE STARTING STRATEGY (If not suitable now, when/where else?).
        - REASONING FOR ANALYSIS.
        
        INPUTS: {idea}, {location}, {target}, Budget: ₹{budget}.
        """
        resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
        full_text = resp.choices[0].message.content.replace("*", "").replace("#", "")
        
        # Structure splitting
        sections = full_text.split("PART")
        st.session_state.report_p1 = sections[1] if len(sections) > 1 else full_text
        st.session_state.report_p2 = sections[2] if len(sections) > 2 else ""
        st.session_state.report_p3 = sections[3] if len(sections) > 3 else ""

# --- PAGE NAVIGATION ---
if st.session_state.report_p1:
    if st.session_state.page == 1:
        st.markdown("## 📊 Page 1: Strategic Intelligence")
        st.markdown(f'<div class="report-box">{st.session_state.report_p1}</div>', unsafe_allow_html=True)
        st.button("Next: Economics & Projections ➡️", on_click=lambda: st.session_state.update({"page": 2}))

    elif st.session_state.page == 2:
        st.markdown("## 💹 Page 2: Financials & Unit Economics")
        
        # Expenditure Chart
        df = pd.DataFrame({
            "Category": ["Infrastructure", "Ops & Staff", "Marketing", "Emergency Reserve"],
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
        st.button("⬅️ Back to Financials", on_click=lambda: st.session_state.update({"page": 2}))
else:
    st.markdown('<div class="report-box" style="text-align:center;">👋 Dashboard Initialized. Enter venture details in the sidebar and click 🔍 GENERATE FULL AUDIT.</div>', unsafe_allow_html=True)
