import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="BizAI | Executive Master", page_icon="💎", layout="wide")

# --- CUSTOM DASHBOARD CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    section[data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.9); }
    [data-testid="stMetric"] { 
        background: rgba(255, 255, 255, 0.03); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        padding: 20px; border-radius: 20px; 
    }
    .main-title {
        background: -webkit-linear-gradient(#38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; text-align: center; margin-bottom: 5px;
    }
    .tagline { color: #94a3b8; font-size: 1.2rem; text-align: center; margin-bottom: 30px; font-style: italic; }
    .report-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 15px; border-left: 5px solid #818cf8; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Lets connect to business world</p>', unsafe_allow_html=True)

# --- SIDEBAR (THE PHONE FIX) ---
with st.sidebar:
    st.markdown("### 🌐 Localization")
    lang = st.radio("Language", ["English", "ಕನ್ನಡ", "हिंदी"], horizontal=True)
    st.markdown("---")
    
    with st.form("executive_master_form"):
        st.markdown("### 🛠 Business Logic")
        idea = st.text_input("Concept Name", placeholder="e.g. Smart EV Solutions")
        location = st.text_input("Location", placeholder="e.g. Bangalore")
        audience = st.text_input("Target Audience", placeholder="e.g. Daily Commuters")
        exp = st.selectbox("Founder Experience", ["Beginner", "Intermediate", "Expert"])
        
        analyze_btn = st.form_submit_button("Launch 360° Analysis", use_container_width=True)
    
    st.caption("RVIM MBA Analytics | Executive Master Version")

# --- ANALYSIS ENGINE ---
if analyze_btn:
    if not idea or not location:
        st.warning("⚠️ Please provide Concept and Location.")
    else:
        with st.spinner("🔄 Drafting Strategic Analysis..."):
            # PROMPT: SWOT, Time, Profit, Risks, Funding, Inspiration, 4Ps, Pitch
            prompt = f"""
            Analyze '{idea}' in '{location}'. Audience: {audience}. Experience: {exp}.
            
            Provide a detailed report including:
            1. FULL SWOT ANALYSIS.
            2. ESTIMATED TIME TO LAUNCH & EXPECTED PROFIT MARGINS (%).
            3. MARKETING MIX (4Ps): Product, Price, Place, Promotion strategy.
            4. FUNDING OPPORTUNITIES (Angel, VC, Crowdfunding, Incubators).
            5. FOUNDER INSPIRATION: Successful founder & their 'Secret Sauce'.
            6. INVESTOR ELEVATOR PITCH: A short, 30-second persuasive pitch.
            7. BRUTALLY HONEST VERDICT in {lang}.
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                report = response.choices[0].message.content

                # Dashboard Metrics (Market Type Removed)
                st.markdown("### 📈 Venture Scorecard")
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Profit Margin", "22-30%", delta="Estimated")
                with m2:
                    st.metric("Time to MVP", "4-5 Months", delta="Setup")
                with m3:
                    st.metric("Success Rate", "68%", delta="High Risk")

                st.markdown("---")
                
                col_left, col_right = st.columns([1.5, 1])
                
                with col_left:
                    st.markdown("#### 📑 Detailed Strategic Assessment")
                    st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                    
                with col_right:
                    # MICRO-ECONOMICS PIE CHART
                    st.markdown("#### 📊 Micro-Economic Resource Split")
                    df_chart = pd.DataFrame({
                        "Factor": ["Labour (Team)", "Land (Rent)", "Capital (Tech)", "Marketing"],
                        "Share": [25, 30, 35, 10]
                    })
                    
                    # Using a safe sequential color scale
                    fig = px.pie(df_chart, values='Share', names='Factor', hole=0.5,
                                 color_discrete_sequence=px.colors.sequential.Turbo)
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', 
                        font=dict(color="white"),
                        margin=dict(t=0,b=0,l=0,r=0), 
                        height=350,
                        showlegend=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info(f"Targeting: {audience if audience else 'General Market'}")
                    st.success(f"Language: {lang}")

            except Exception as e:
                st.error(f"Error during analysis: {e}")
else:
    # Landing Page
    st.markdown(f"""
        <div style="text-align: center; padding: 60px;">
            <h2 style="color: #94a3b8;">Strategic Venture Control Hub</h2>
            <p style="color: #64748b;">Ready to analyze <b>{idea if idea else 'your venture'}</b> for <b>{location if location else 'any market'}</b>.</p>
        </div>
    """, unsafe_allow_html=True)
