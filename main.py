import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- MOBILE-STABLE & EXECUTIVE CONFIG ---
st.set_page_config(page_title="BizVenture Pro", page_icon="🔍", layout="centered")

# --- EXECUTIVE THEME & MOBILE UI FIX ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f1f5f9; }
    section[data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; }
    [data-testid="stMetric"] { background: #1e293b; border: 1px solid #38bdf8; padding: 15px; border-radius: 12px; }
    .report-box { background: #1e293b; color: #ffffff !important; padding: 25px; border-radius: 12px; border: 1px solid #334155; font-size: 1.1rem; line-height: 1.8; }
    .main-title { color: #38bdf8; font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 0px; }
    .tagline { color: #64748b; font-size: 1.1rem; text-align: center; margin-bottom: 30px; }
    .stButton>button { border-radius: 20px; font-weight: bold; background-color: #38bdf8 !important; color: #020617 !important; width: 100%; height: 3.2em; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (3-PAGE ARCHITECTURE) ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

st.markdown('<h1 class="main-title">BizVenture</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Connect to the business world</p>', unsafe_allow_html=True)

# --- SIDEBAR: DISCOVERY CONSOLE ---
with st.sidebar:
    st.markdown('### 🔍 Search Console')
    lang = st.radio("Language", ["English", "हिंदी"], horizontal=True)
    st.markdown("---")
    idea = st.text_input("Venture Idea", placeholder="e.g. EV Hub")
    location = st.text_input("Location", placeholder="e.g. Bangalore")
    target = st.text_input("Target Audience", placeholder="e.g. Students")
    budget = st.number_input("Capital (₹)", min_value=10000, value=500000)
    industry = st.selectbox("Industry", ["Retail", "Tech", "Manufacturing", "Food & Beverage", "Service"])
    stage = st.selectbox("Venture Stage", ["MVP/Testing", "Market Entry", "Scaling"])
    
    if st.button("🚀 ANALYZE VENTURE"):
        st.session_state.page = 1
        with st.spinner("🤖 Consulting Strategy Data..."):
            prompt = f"""
            SYSTEM: You are a professional MBA Executive Consultant. You must use PERFECT SPELLING and professional grammar. Do not mention specific markets like Sultanpete.
            
            INPUT: Idea: {idea}, Location: {location}, Target: {target}, Budget: ₹{budget}, Industry: {industry}, Stage: {stage}, Language: {lang}.
            
            REPORT STRUCTURE:
            PART 1 (STRATEGY): Detailed SWOT and 4Ps Marketing Mix for {target}.
            PART 2 (GROWTH): Success Rate (%), ROI Timeline, and Funding Roadmap. List specific projected Profits and Expenses for Year 2 and Year 3.
            PART 3 (RISK): A detailed 'Loss Recovery Plan' on how to regain market share if the business faces a loss. Finish with a 30-second Investor Pitch.
            """
            resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
            st.session_state.report = resp.choices[0].message.content

# --- PAGE 1: STRATEGIC DISCOVERY ---
if st.session_state.page == 1:
    if st.session_state.report:
        st.markdown("### 📋 Step 1: Strategic Discovery")
        c1, c2, c3 = st.columns(3)
        c1.metric("Capital", f"₹{budget:,}")
        c2.metric("Industry", industry)
        c3.metric("Stage", stage)
        
        # Display Strategy Part
        content = st.session_state.report.split("PART 2")[0]
        st.markdown(f'<div class="report-box">{content}</div>', unsafe_allow_html=True)
        st.button("Next: Financial Dashboard ➡️", on_click=lambda: st.session_state.update({"page": 2}))
    else:
        st.info("Enter details in the sidebar and click 'Analyze Venture' to begin!")

# --- PAGE 2: FINANCIAL DASHBOARD ---
elif st.session_state.page == 2:
    st.markdown("### 💹 Step 2: Capital Allocation")
    
    allocs = [0.4, 0.25, 0.2, 0.15]
    side_df = pd.DataFrame({"Category": ["Setup", "Ops", "Marketing", "Reserve"], "Amount": [budget*a for a in allocs]})
    
    # Pie Chart - Legend at bottom to prevent mobile overlap
    fig = px.pie(side_df, values='Amount', names='Category', hole=0.5, color_discrete_sequence=px.colors.sequential.Tealgrn)
    fig.update_layout(
        showlegend=True, 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color="white"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
        margin=dict(t=10, b=100, l=10, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.table(side_df.style.format({"Amount": "₹{:,.0f}"}))
    st.button("Next: The Final Verdict ➡️", on_click=lambda: st.session_state.update({"page": 3}))
    st.button("⬅️ Back to Strategy", on_click=lambda: st.session_state.update({"page": 1}))

# --- PAGE 3: THE VERDICT & RISK ---
elif st.session_state.page == 3:
    st.markdown("### 🏆 Step 3: Performance & Risk")
    
    # Display the rest of the report (Growth & Risk)
    report_text = st.session_state.report
    if "PART 2" in report_text:
        display_content = "PART 2" + report_text.split("PART 2")[-1]
    else:
        display_content = report_text
        
    st.markdown(f'<div class="report-box">{display_content}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.download_button(label="📄 Download Complete Report", data=st.session_state.report, file_name=f"BizVenture_Report.txt")
    st.button("⬅️ Back to Financials", on_click=lambda: st.session_state.update({"page": 2}))
