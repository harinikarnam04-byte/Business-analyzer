import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- CONFIG: MOBILE STABLE & EXECUTIVE ---
st.set_page_config(page_title="BizVenture Ultimate", page_icon="🔍", layout="centered")

# --- UI THEME: EXECUTIVE NAVY ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f1f5f9; }
    section[data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; }
    [data-testid="stMetric"] { background: #1e293b; border: 1px solid #38bdf8; padding: 15px; border-radius: 12px; }
    .report-box { background: #1e293b; color: #ffffff !important; padding: 25px; border-radius: 12px; border: 1px solid #334155; font-size: 1.1rem; line-height: 1.8; }
    .main-title { color: #38bdf8; font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 0px; }
    .tagline { color: #64748b; font-size: 1.1rem; text-align: center; margin-bottom: 30px; font-style: italic; }
    .stButton>button { border-radius: 20px; font-weight: bold; background-color: #38bdf8 !important; color: #020617 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE MANAGEMENT ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

st.markdown('<h1 class="main-title">BizVenture</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Lets connect to business world</p>', unsafe_allow_html=True)

# --- SIDEBAR: THE DISCOVERY CONSOLE ---
with st.sidebar:
    st.markdown('### 🔍 Search Console')
    lang = st.radio("Language / भाषा", ["English", "हिंदी"], horizontal=True)
    st.markdown("---")
    
    idea = st.text_input("Business Idea", placeholder="e.g. EV Charging / Organic Cafe")
    location = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. Gen Z / Professionals")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    
    industry = st.selectbox("Industry Benchmark", ["Retail/E-commerce", "Manufacturing", "Tech/SaaS", "Food & Beverage", "Service Sector"])
    stage = st.selectbox("Venture Stage", ["MVP (Testing Phase)", "Early Traction (Market Entry)", "Scaling (High Growth)"])
    
    # --- DYNAMIC FINANCIAL LOGIC ---
    # Base allocations per industry
    alloc_map = {
        "Retail/E-commerce": [0.4, 0.25, 0.2, 0.15],
        "Manufacturing": [0.6, 0.2, 0.1, 0.1],
        "Tech/SaaS": [0.2, 0.2, 0.5, 0.1],
        "Food & Beverage": [0.45, 0.25, 0.2, 0.1],
        "Service Sector": [0.2, 0.3, 0.3, 0.2]
    }
    base = alloc_map[industry]
    
    # Adjusting based on Stage (Scaling needs more marketing)
    if stage == "Scaling (High Growth)":
        base[2] += 0.15; base[0] -= 0.15
    elif stage == "MVP (Testing Phase)":
        base[0] += 0.10; base[2] -= 0.10

    side_df = pd.DataFrame({
        "Category": ["Product Setup", "Operations", "Marketing", "Cash Reserve"],
        "₹ Amount": [budget*base[0], budget*base[1], budget*base[2], budget*base[3]]
    })

    st.markdown("---")
    if st.button("🚀 GET STRATEGY", use_container_width=True):
        st.session_state.page = 1
        with st.spinner("🤖 Consulting Business Data..."):
            prompt = f"""
            MBA Consultant Role. Venture: {idea} in {location}. Industry: {industry}. Stage: {stage}. Target: {target}. Budget: ₹{budget}. Language: {lang}. 
            
            Strictly include:
            1. Professional SWOT Analysis.
            2. Marketing Mix (4Ps) tailored to {target}.
            3. Bangalore Local Intelligence (reference hubs like Sultanpete, Jayanagar, or Manyata).
            4. Funding Roadmap: Angel, VC, or Debt advice for the {stage} phase.
            5. ROI Estimates, Success Probability %, and Profit Margins.
            6. 30-Second Investor Pitch and Final Verdict in {lang}.
            """
            resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
            st.session_state.report = resp.choices[0].message.content

# --- PAGE 1: STRATEGY DASHBOARD ---
if st.session_state.page == 1:
    if st.session_state.report:
        st.markdown(f"### 📋 Step 1: {stage} Strategic Analysis")
        c1, c2, c3 = st.columns(3)
        c1.metric("Capital", f"₹{budget:,}")
        c2.metric("Industry", industry.split('/')[0])
        c3.metric("Stage", stage.split(' ')[0])
        
        st.markdown(f'<div class="report-box">{st.session_state.report}</div>', unsafe_allow_html=True)
        st.button("Next: Financial Execution ➡️", on_click=lambda: st.session_state.update({"page": 2}), use_container_width=True)
    else:
        st.info("Enter your venture details in the Search Console to begin.")

# --- PAGE 2: FINANCIAL DASHBOARD ---
elif st.session_state.page == 2:
    st.markdown("### 💹 Step 2: Financial Strategy Dashboard")
    
    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        fig = px.pie(side_df, values='₹ Amount', names='Category', hole=0.5, color_discrete_sequence=px.colors.sequential.Tealgrn)
        fig.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), margin=dict(t=0,b=0,l=0,r=0), height=350, legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.markdown(f"#### {industry} Allocation")
        st.table(side_df.style.format({"₹ Amount": "₹{:,.0f}"}))
    
    st.markdown("---")
    st.download_button(label="📄 Download Business Report", data=st.session_state.report, file_name=f"BizVenture_{idea}.txt", use_container_width=True)
    st.button("⬅️ Back to Strategy", on_click=lambda: st.session_state.update({"page": 1}), use_container_width=True)
