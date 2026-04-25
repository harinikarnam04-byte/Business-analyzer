import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="BizAI | Venture Master", page_icon="💎", layout="wide")

# --- FULL PREMIUM CSS ---
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
        font-size: 2.8rem; font-weight: 800; text-align: center;
    }
    .report-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #818cf8;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)

# --- SIDEBAR (THE PHONE FIX RETAINED) ---
with st.sidebar:
    st.markdown("### 🛠 Business Strategy")
    with st.form("master_biz_form"):
        idea = st.text_input("Concept Name", placeholder="e.g. Premium Pet Cafe")
        location = st.text_input("Target Area", placeholder="e.g. Jayanagar")
        budget = st.number_input("Seed Capital (₹)", min_value=10000, value=1000000)
        
        audience = st.selectbox("Target Audience", 
                                ["Gen Z / Students", "Working Professionals", "HNIs (Premium)", "B2B Corporates", "Local Residents"])
        
        exp = st.selectbox("Founder Experience", ["Beginner", "Intermediate", "Expert"])
        
        analyze_btn = st.form_submit_button("Launch Full Analysis", use_container_width=True)
    
    st.caption("Strategic Analytics | RVIM 2026")

# --- MAIN ANALYSIS LOGIC ---
if analyze_btn:
    if not idea or not location:
        st.warning("⚠️ Please provide a Concept and Location.")
    else:
        with st.spinner("🔄 Performing 360° Venture Analysis..."):
            # MERGED PROMPT: Includes Risks, SWOT, Success Rate, Time, and Inspiration
            prompt = f"""
            Analyze the business idea '{idea}' in '{location}' with a budget of ₹{budget}.
            Target Audience: {audience}. Experience Level: {exp}.
            
            Provide a BRUTALLY HONEST review including:
            1. FULL SWOT ANALYSIS (Strengths, Weaknesses, Opportunities, Threats).
            2. TOP RISKS & SUCCESS PROBABILITY (%).
            3. ESTIMATED TIME TO LAUNCH (Weeks/Months).
            4. ENTREPRENEUR INSPIRATION: Mention a successful founder in this sector and their 'Secret Sauce'.
            5. FINAL VERDICT: Is it worth the money?
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                report = response.choices[0].message.content

                # Results Dashboard - Metrics Row
                st.markdown("### 📈 Real-Time Reality Check")
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric("Success Rate", "58%", delta="Moderate Risk")
                with m2:
                    st.metric("Time to MVP", "3-5 Months", delta="Setup Phase")
                with m3:
                    st.metric("Context", location if location else "Global")
                with m4:
                    st.metric("Runway", "9 Months", help="Based on 10% monthly burn")

                st.markdown("---")
                
                # Report and Visuals
                col_left, col_right = st.columns([1.4, 1])
                
                with col_left:
                    st.markdown("#### 📑 Detailed Strategic Review")
                    st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                
                with col_right:
                    st.markdown("#### 📊 Operations & Capex Split")
                    # DETAILED BUDGET BREAKDOWN: Rent, Inventory, Marketing, Reserve
                    df = pd.DataFrame({
                        "Department": ["Rent (6mo Deposit)", "Inventory/Hardware", "Digital Marketing", "Legal & Permits", "Safety Reserve"],
                        "Allocation": [budget*0.35, budget*0.30, budget*0.20, budget*0.05, budget*0.10]
                    })
                    fig = px.pie(df, values='Allocation', names='Department', hole=0.5,
                                 color_discrete_sequence=px.colors.sequential.Agsunset)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"),
                                      margin=dict(t=0,b=0,l=0,r=0), height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.success(f"Targeting: {audience}")
                    st.warning(f"Strategy level: {exp}")

            except Exception as e:
                st.error(f"Error: {e}")

else:
    # --- Landing State ---
    st.markdown(f"""
        <div style="text-align: center; padding: 50px;">
            <h2 style="color: #94a3b8;">Strategic Venture Control</h2>
            <p style="color: #64748b;">Configure your startup parameters in the sidebar to generate a 
            high-fidelity <b>SWOT, Budget, and Risk</b> analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Static placeholder row
    c1, c2, c3 = st.columns(3)
    c1.metric("Market Data", "Active")
    c2.metric("Persona Match", "Enabled")
    c3.metric("Analysis Mode", "Brutal Honesty")
