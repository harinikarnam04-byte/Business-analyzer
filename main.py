import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- MOBILE-STABLE & EXECUTIVE CONFIG ---
st.set_page_config(page_title="BizVenture", page_icon="🔍", layout="centered")

# --- EXECUTIVE NAVY THEME (HIGH CONTRAST) ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f1f5f9; }
    section[data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; }
    
    /* High Contrast Metrics */
    [data-testid="stMetric"] { 
        background: #1e293b; 
        border: 1px solid #38bdf8; 
        padding: 15px; border-radius: 12px; 
    }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 800; }
    
    /* Report Box: No hidden text */
    .report-box { 
        background: #1e293b; 
        color: #ffffff !important; 
        padding: 25px; border-radius: 12px; 
        border: 1px solid #334155; 
        font-size: 1.1rem; line-height: 1.8; 
    }
    
    .main-title { color: #38bdf8; font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 0px; }
    .tagline { color: #64748b; font-size: 1.1rem; text-align: center; margin-bottom: 30px; font-style: italic; }
    
    .stButton>button { border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (Multi-Page Logic) ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

st.markdown('<h1 class="main-title">BizVenture</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Lets connect to business world</p>', unsafe_allow_html=True)

# --- SIDEBAR: DISCOVERY CONSOLE ---
with st.sidebar:
    st.markdown('### 🔍 Search Console')
    lang = st.radio("Language / भाषा", ["English", "हिंदी"], horizontal=True)
    
    st.markdown("---")
    idea = st.text_input("Business Idea", placeholder="e.g. EV Charging")
    location = st.text_input("Location", placeholder="e.g. Bangalore")
    budget = st.number_input("Budget (₹)", min_value=10000, value=500000)
    
    # SIMPLE STRATEGY SLIDER (Drives AI and Math)
    mode = st.select_slider("Strategy Mode", options=["Safe", "Balanced", "Growth"])
    
    # Dynamic Math Logic for Sidebar Chart
    if mode == "Growth": allocs = [0.3, 0.2, 0.4, 0.1] 
    elif mode == "Safe": allocs = [0.4, 0.3, 0.1, 0.2]
    else: allocs = [0.4, 0.25, 0.2, 0.15] # Balanced

    st.markdown("#### 📊 Live Budget Split")
    side_df = pd.DataFrame({
        "Category": ["Setup", "Ops", "Marketing", "Reserve"],
        "₹ Amount": [budget*allocs[0], budget*allocs[1], budget*allocs[2], budget*allocs[3]]
    })
    
    fig_side = px.pie(side_df, values='₹ Amount', names='Category', hole=0.6, 
                      color_discrete_sequence=px.colors.sequential.Tealgrn)
    fig_side.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', 
                           margin=dict(t=0,b=0,l=0,r=0), height=180)
    st.plotly_chart(fig_side, use_container_width=True)
    
    st.markdown("---")
    if st.button("🔍 GET STRATEGY", use_container_width=True):
        st.session_state.page = 1
        with st.spinner("🤖 Simulating Business Model..."):
            prompt = f"""
            Act as an MBA Venture Consultant. 
            Venture: {idea} in {location}. Budget: ₹{budget}. Mode: {mode}. Language: {lang}. 
            
            Deliver:
            1. SWOT Analysis & 4Ps Marketing Mix.
            2. Bangalore-Specific Context (referencing hubs like Jayanagar/Sultanpete).
            3. ROI Timeline & Success Score.
            4. Founder Inspiration & 30-Second Investor Pitch.
            5. Final Verdict in {lang}.
            """
            resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
            st.session_state.report = resp.choices[0].message.content

# --- PAGE 1: STRATEGY ---
if st.session_state.page == 1:
    if st.session_state.report:
        st.markdown("### 📋 Step 1: Strategic Discovery")
        c1, c2, c3 = st.columns(3)
        c1.metric("Capital", f"₹{budget:,}")
        c2.metric("Mode", mode)
        c3.metric("Status", "High Potential")
        
        st.markdown(f'<div class="report-box">{st.session_state.report}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.button("Next: Financial Execution ➡️", on_click=lambda: st.session_state.update({"page": 2}), use_container_width=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 60px; border: 2px dashed #1e293b; border-radius: 20px;">
                <span style="font-size: 50px;">🔍</span>
                <h3 style="color: #38bdf8;">Discovery Console Ready</h3>
                <p style="color: #94a3b8;">Enter your idea in the sidebar and click <b>Get Strategy</b>.<br>Watch the sidebar chart update as you change modes!</p>
            </div>
        """, unsafe_allow_html=True)

# --- PAGE 2: FINANCIALS & EXPORT ---
elif st.session_state.page == 2:
    st.markdown("### 💹 Step 2: Financial Execution")
    
    st.markdown("#### Industry-Weighted Budget Allocation")
    st.table(side_df.style.format({"₹ Amount": "₹{:,.2f}"}))
    
    st.markdown("---")
    st.markdown("#### 📥 Finalize & Download")
    full_text = f"BIZVENTURE EXECUTIVE SUMMARY\n{'='*30}\nIdea: {idea}\nLocation: {location}\nBudget: ₹{budget}\nMode: {mode}\n\n{st.session_state.report}"
    
    st.download_button(
        label="📄 Download Business Report",
        data=full_text,
        file_name=f"BizVenture_{idea}.txt",
        use_container_width=True
    )
    
    st.button("⬅️ Back to Strategy", on_click=lambda: st.session_state.update({"page": 1}), use_container_width=True)
