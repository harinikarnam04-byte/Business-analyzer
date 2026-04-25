import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- MOBILE-FIRST ARCHITECTURE ---
st.set_page_config(page_title="BizAI Venture Consultant", page_icon="💎", layout="centered")

# --- HIGH-READABILITY EXECUTIVE NAVY THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f1f5f9; }
    section[data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; }
    
    /* High-contrast Metric Cards */
    [data-testid="stMetric"] { 
        background: #1e293b; 
        border: 1px solid #38bdf8; 
        padding: 15px; border-radius: 12px; 
    }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 800; }
    [data-testid="stMetricLabel"] { color: #38bdf8 !important; }

    .main-title {
        background: -webkit-linear-gradient(#38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem; font-weight: 800; text-align: center; margin-bottom: 0px;
    }
    .tagline { color: #64748b; font-size: 1rem; text-align: center; margin-bottom: 20px; font-style: italic; }

    /* Report Box: No hidden text, clear white on navy */
    .report-box {
        background: #1e293b;
        color: #ffffff !important;
        padding: 25px; border-radius: 12px; 
        border: 1px solid #334155;
        font-size: 1.1rem; line-height: 1.8;
    }
    
    /* Start Guidance */
    .start-label { color: #38bdf8; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Lets connect to business world</p>', unsafe_allow_html=True)

# --- SIDEBAR (MOBILE-STABLE INPUTS) ---
with st.sidebar:
    st.markdown('<p class="start-label">⬇ START HERE / यहाँ शुरू करें</p>', unsafe_allow_html=True)
    lang = st.radio("Language / भाषा", ["English", "हिंदी"], horizontal=True)
    st.markdown("---")
    
    idea = st.text_input("Business Idea", placeholder="e.g. Smart Logistics")
    location = st.text_input("Location", placeholder="e.g. Bangalore")
    budget = st.number_input("Investment (₹)", min_value=5000, value=500000, step=5000)
    
    with st.expander("Strategy Details"):
        audience = st.text_input("Target Audience", placeholder="e.g. SME Owners")
        exp = st.selectbox("Founder Experience", ["Beginner", "Intermediate", "Expert"])
    
    st.markdown("---")
    # Trigger for Mobile stability
    generate = st.button("🚀 GENERATE STRATEGY", use_container_width=True)
    st.caption("RVIM MBA Analytics • Executive Final")

# --- CORE ENGINE (CONTEXTUAL TRANSCREATION) ---
if generate:
    if not idea or not location:
        st.warning("⚠️ Please provide an Idea and Location.")
    else:
        with st.spinner("🔄 AI Consultant is modeling your venture..."):
            
            # Natural Intent Prompt Logic
            prompt = f"""
            Role: Senior MBA Venture Consultant. Output Language: {lang}.
            Venture: {idea} in {location}. Budget: ₹{budget}. Audience: {audience}.
            
            CRITICAL: If language is 'हिंदी', use professional business Hindi (Transcreation, not literal translation).
            
            Structure:
            1. FULL SWOT ANALYSIS.
            2. MARKETING MIX (4Ps).
            3. FINANCIAL MATH: Spend breakdown of ₹{budget} with actual ₹ figures.
            4. PERFORMANCE: Profit %, Launch Time, Success Probability.
            5. FUNDING & INSPIRATION: Angel/VC paths + Founder 'Secret Sauce'.
            6. INVESTOR ELEVATOR PITCH (30-second script).
            7. BRUTALLY HONEST VERDICT in {lang}.
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                report = response.choices[0].message.content

                # Vertical Stack for Mobile Scorecard
                st.metric("Total Investment", f"₹{budget:,}")
                st.metric("Exp. Profit Margin", "22-30%")
                st.metric("Timeline to Launch", "4-6 Months")

                st.markdown("---")
                
                # Report Section
                st.markdown(f"### 📋 Strategic Roadmap ({lang})")
                st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Math & Resource Chart
                st.markdown("### 💹 Capital Allocation (Math)")
                math_df = pd.DataFrame({
                    "Category": ["Setup/CapEx", "Inventory/Ops", "Marketing", "Cash Reserve"],
                    "Amount (₹)": [budget*0.4, budget*0.25, budget*0.2, budget*0.15]
                })
                st.table(math_df)

                # Micro-Economic Resource Split
                fig = px.pie(math_df, values='Amount (₹)', names='Category', hole=0.5,
                             color_discrete_sequence=px.colors.sequential.GnBu_r)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"),
                                  margin=dict(t=20,b=20,l=20,r=20), height=350)
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Analysis Error: {e}")
else:
    # Clean Initial State
    st.markdown(f"""
        <div style="text-align: center; padding: 60px; border: 2px dashed #1e293b; border-radius: 20px;">
            <h3 style="color: #38bdf8;">Strategic Hub Ready</h3>
            <p style="color: #94a3b8;">Fill the sidebar details and click <b>Generate</b> to see your 360° Business Strategy.</p>
        </div>
    """, unsafe_allow_html=True)
