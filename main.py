import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="BizAI | Venture Consultant", page_icon="💎", layout="wide")

# --- HIGH READABILITY DASHBOARD CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    section[data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #333; }
    [data-testid="stMetric"] { background: #111111; border: 1px solid #38bdf8; padding: 20px; border-radius: 15px; }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; }
    [data-testid="stMetricLabel"] { color: #38bdf8 !important; }
    .main-title { color: #38bdf8; font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 0px; }
    .tagline { color: #888888; font-size: 1.1rem; text-align: center; margin-bottom: 25px; }
    .report-box { background: #000000; color: #FFFFFF !important; padding: 30px; border: 1px solid #444; border-radius: 15px; line-height: 1.8; font-size: 1.1rem; }
    .start-label { color: #38bdf8; font-weight: bold; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Lets connect to business world</p>', unsafe_allow_html=True)

# --- SIDEBAR (THE AUTO-TRIGGER INPUTS) ---
with st.sidebar:
    st.markdown('<p class="start-label">⬇ START HERE / यहाँ शुरू करें</p>', unsafe_allow_html=True)
    lang = st.radio("Language / भाषा", ["English", "हिंदी"], horizontal=True)
    st.markdown("---")
    
    # Input triggers
    idea = st.text_input("Business Idea", placeholder="e.g. Cloud Kitchen")
    location = st.text_input("Location", placeholder="e.g. Jayanagar, Bangalore")
    budget = st.number_input("Investment (₹)", min_value=5000, value=500000)
    audience = st.text_input("Target Audience", placeholder="e.g. Working Professionals")
    exp = st.selectbox("Founder Experience", ["Beginner", "Intermediate", "Expert"])
    
    st.markdown("---")
    st.caption("RVIM MBA Analytics • Auto-Trigger Mode")

# --- AUTO-ANALYSIS LOGIC ---
# The analysis starts automatically if 'idea' and 'location' have text
if idea and location:
    with st.spinner("🤖 AI Consultant is analyzing your venture..."):
        # THE ALL-IN-ONE PROMPT (No features lost)
        prompt_instruction = f"""
        Role: Senior Business Consultant. 
        Language: {lang}. (If Hindi, use natural, professional business Hindi terms).
        
        Venture: {idea} in {location}.
        Budget: ₹{budget}. Audience: {audience}. Experience: {exp}.
        
        Provide:
        1. SWOT ANALYSIS (Strengths, Weaknesses, Opportunities, Threats).
        2. 4Ps MARKETING MIX (Product, Price, Place, Promotion).
        3. FINANCIAL MATH: Allocate the ₹{budget} budget (show specific ₹ amounts).
        4. PERFORMANCE: Expected Profit %, Launch Time, Success Probability.
        5. FUNDING & INSPIRATION: Angel/VC paths + Founder 'Secret Sauce'.
        6. INVESTOR PITCH: 30-second persuasive pitch.
        7. FINAL VERDICT in {lang}.
        """
        
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt_instruction}]
            )
            report = response.choices[0].message.content

            # Dashboard metrics
            st.markdown("### 📈 Venture Scorecard")
            m1, m2, m3 = st.columns(3)
            with m1: st.metric("Investment", f"₹{budget:,}")
            with m2: st.metric("Exp. Profit", "22-30%", delta="Target")
            with m3: st.metric("Time to MVP", "4-6 Months", delta="Planned")

            st.markdown("---")
            
            col_left, col_right = st.columns([1.7, 1])
            with col_left:
                st.markdown(f"#### 📋 Strategic Dashboard ({lang})")
                st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                
            with col_right:
                st.markdown("#### 💹 Fund Allocation (Math)")
                math_df = pd.DataFrame({
                    "Category": ["Setup", "Inventory", "Marketing", "Reserve"],
                    "Amount (₹)": [budget*0.4, budget*0.25, budget*0.2, budget*0.15]
                })
                st.table(math_df)

                fig = px.pie(math_df, values='Amount (₹)', names='Category', hole=0.5,
                             color_discrete_sequence=px.colors.qualitative.Bold)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"),
                                  margin=dict(t=0,b=0,l=0,r=0), height=300)
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Analysis Error: {e}")
else:
    # Empty State (Before user types anything)
    st.markdown(f"""
        <div style="text-align: center; padding: 100px; border: 2px dashed #333; border-radius: 20px;">
            <h2 style="color: #38bdf8;">Strategic Hub Ready</h2>
            <p style="color: #FFFFFF;">The report will <b>automatically pop up</b> once you type your Idea and Location.</p>
            <p style="color: #555;">जैसे ही आप अपना विचार और स्थान टाइप करेंगे, रिपोर्ट अपने आप आ जाएगी।</p>
        </div>
    """, unsafe_allow_html=True)
