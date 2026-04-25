import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- MOBILE-READY & EXECUTIVE CONFIG ---
st.set_page_config(page_title="BizAI Executive", page_icon="🔍", layout="centered")

# --- EXECUTIVE NAVY & NEON THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f1f5f9; }
    section[data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; }
    [data-testid="stMetric"] { background: #1e293b; border: 1px solid #38bdf8; padding: 15px; border-radius: 12px; }
    .report-box { background: #1e293b; color: #ffffff !important; padding: 25px; border-radius: 12px; border: 1px solid #334155; font-size: 1.1rem; line-height: 1.8; }
    .main-title { background: -webkit-linear-gradient(#38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.2rem; font-weight: 800; text-align: center; }
    .stButton>button { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE FOR MULTI-PAGE UX ---
if 'page' not in st.session_state: st.session_state.page = 1
if 'report' not in st.session_state: st.session_state.report = ""

def go_to_page2(): st.session_state.page = 2
def go_to_page1(): st.session_state.page = 1

st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)

# --- SIDEBAR: DISCOVERY CONSOLE & SIDE-CHART ---
with st.sidebar:
    st.markdown('### 🔍 DISCOVERY CONSOLE')
    lang = st.radio("Language / भाषा", ["English", "हिंदी"], horizontal=True)
    
    st.markdown("---")
    industry = st.selectbox("Industry Benchmark", ["Retail/E-commerce", "Manufacturing", "Tech/SaaS", "Food & Beverage", "Service Sector"])
    idea = st.text_input("Venture Idea", placeholder="e.g. EV Charging")
    location = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    budget = st.number_input("Investment (₹)", min_value=10000, value=500000)
    
    mkt_intensity = st.select_slider("Marketing Aggression", options=["Conservative", "Balanced", "Aggressive"])
    
    # DYNAMIC SIDEBAR PIE CHART (Industry Weighted)
    st.markdown("#### 📊 Real-time Budget Split")
    allocs = {"Retail/E-commerce": [0.3, 0.4, 0.2, 0.1], "Manufacturing": [0.6, 0.2, 0.1, 0.1], 
              "Tech/SaaS": [0.2, 0.2, 0.5, 0.1], "Food & Beverage": [0.4, 0.3, 0.2, 0.1], "Service Sector": [0.2, 0.2, 0.4, 0.2]}
    base = allocs[industry]
    
    side_df = pd.DataFrame({
        "Category": ["Setup", "Ops", "Mkt", "Reserve"],
        "Amount": [budget*base[0], budget*base[1], budget*base[2], budget*base[3]]
    })
    
    fig_side = px.pie(side_df, values='Amount', names='Category', hole=0.6,
                      color_discrete_sequence=px.colors.sequential.Tealgrn)
    fig_side.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), height=200)
    st.plotly_chart(fig_side, use_container_width=True)
    
    st.markdown("---")
    if st.button("🚀 GENERATE STRATEGY", use_container_width=True):
        st.session_state.page = 1
        with st.spinner("🤖 Consulting AI Expert..."):
            prompt = f"MBA Consultant. Language: {lang}. Analyze {idea} in {location} with ₹{budget}. Industry: {industry}. Strategy: {mkt_intensity}. Include Bangalore-specific intelligence, SWOT, 4Ps, ROI, and Investor Pitch."
            resp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
            st.session_state.report = resp.choices[0].message.content

# --- PAGE 1: STRATEGIC DASHBOARD ---
if st.session_state.page == 1:
    if st.session_state.report:
        st.markdown("### 📋 Page 1: Strategic Analysis")
        c1, c2, c3 = st.columns(3)
        c1.metric("Capital", f"₹{budget:,}")
        c2.metric("Success", "78%", delta="High")
        c3.metric("Industry", industry.split('/')[0])
        
        st.markdown(f'<div class="report-box">{st.session_state.report}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.button("Next: Financials & Export ➡️", on_click=go_to_page2, use_container_width=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 60px; border: 2px dashed #1e293b; border-radius: 20px;">
                <span style="font-size: 50px;">🔍</span>
                <h3 style="color: #38bdf8;">Venture Intelligence Ready</h3>
                <p style="color: #94a3b8;">Enter details in the Discovery Console.<br>Check the sidebar for your real-time budget split.</p>
            </div>
        """, unsafe_allow_html=True)

# --- PAGE 2: EXECUTION & PDF ---
elif st.session_state.page == 2:
    st.markdown("### 💹 Page 2: Financial Execution")
    
    st.markdown("#### Capital Allocation Table")
    st.table(side_df.rename(columns={"Amount": "Amount (₹)"}))
    
    st.markdown("---")
    st.markdown("#### 📥 Finalize Report")
    full_text = f"BIZAI EXECUTIVE SUMMARY\nVenture: {idea}\nLocation: {location}\nBudget: ₹{budget}\n\n{st.session_state.report}"
    
    st.download_button(
        label="📄 Download PDF / Report",
        data=full_text,
        file_name=f"BizAI_{idea}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.button("⬅️ Back to Strategy", on_click=go_to_page1, use_container_width=True)
