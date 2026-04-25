import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="BizAI Venture Consultant", page_icon="💎", layout="wide")

# --- FULL PREMIUM UI ARCHITECTURE ---
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
    .stTable { background-color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Lets connect to business world</p>', unsafe_allow_html=True)

# --- SIDEBAR (THE PHONE FIX & INPUTS) ---
with st.sidebar:
    st.markdown("### 🌐 Localization")
    lang = st.radio("Language / भाषा", ["English", "हिंदी"], horizontal=True)
    st.markdown("---")
    
    with st.form("ultimate_master_archive_form"):
        st.markdown("### 🛠 Project Setup")
        idea = st.text_input("Business Concept", placeholder="e.g. Organic Soap Brand")
        location = st.text_input("Target Area", placeholder="e.g. Jayanagar, Bangalore")
        budget = st.number_input("Investment Amount (₹)", min_value=5000, value=500000)
        audience = st.text_input("Target Audience", placeholder="e.g. Eco-conscious youth")
        exp = st.selectbox("Founder Experience", ["Beginner", "Intermediate", "Expert"])
        
        analyze_btn = st.form_submit_button("Launch 360° Analysis", use_container_width=True)
    
    st.caption("RVIM MBA Analytics • All Features Integrated")

# --- ANALYSIS ENGINE ---
if analyze_btn:
    if not idea or not location:
        st.warning("⚠️ Please provide Concept and Location.")
    else:
        with st.spinner("🔄 Deep-Diving into Math & Strategy..."):
            # THE COMPLETE PROMPT (NOTHING LOST)
            prompt = f"""
            Perform a professional venture analysis for '{idea}' in '{location}'.
            Investment: ₹{budget}. Audience: {audience}. Experience: {exp}. 
            Language: {lang}.
            
            Deliver a report covering:
            1. FULL SWOT ANALYSIS (Strengths, Weaknesses, Opportunities, Threats).
            2. 4Ps MARKETING MIX (Product, Price, Place, Promotion).
            3. FINANCIAL MATH: Break down the ₹{budget} budget into specific ₹ figures for Setup, Marketing, and Operations.
            4. PERFORMANCE METRICS: Estimated Time to Launch, Profit Margin (%), and Success Probability.
            5. FUNDING & INSPIRATION: Suggest Angel/VC/Crowdfunding paths + A successful founder's 'Secret Sauce'.
            6. INVESTOR ELEVATOR PITCH: 30-second persuasive script.
            7. BRUTALLY HONEST VERDICT in {lang}.
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                report = response.choices[0].message.content

                # 📊 Dashboard Row
                st.markdown("### 📈 Venture Scorecard")
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Total CapEx", f"₹{budget:,}")
                with m2:
                    st.metric("Exp. Profit %", "22-30%", delta="Industry Avg")
                with m3:
                    st.metric("Time to MVP", "4-6 Months", delta="Planned")

                st.markdown("---")
                
                # 📑 Strategy & Report Row
                col_left, col_right = st.columns([1.5, 1])
                
                with col_left:
                    st.markdown(f"#### 📋 Strategy & Financial Report ({lang})")
                    st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                    
                with col_right:
                    # FINANCIAL MATH (PRACTICAL FIGURES)
                    st.markdown("#### 💹 Fund Allocation (Math)")
                    math_data = pd.DataFrame({
                        "Category": ["CapEx / Setup", "Inventory / Tech", "Marketing", "Cash Reserve"],
                        "Share %": [40, 25, 20, 15],
                        "Amount (₹)": [budget*0.4, budget*0.25, budget*0.2, budget*0.15]
                    })
                    st.table(math_data)

                    # MICRO-ECONOMIC PIE CHART
                    st.markdown("#### 📊 Factors of Production")
                    fig = px.pie(math_data, values='Share %', names='Category', hole=0.5,
                                 color_discrete_sequence=px.colors.sequential.Agsunset)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"),
                                      margin=dict(t=0,b=0,l=0,r=0), height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.success(f"Output Language: {lang}")
                    st.info(f"Targeting: {audience if audience else 'Mass Market'}")

            except Exception as e:
                st.error(f"Error: {e}")
else:
    # Landing Page
    st.markdown(f"""
        <div style="text-align: center; padding: 60px;">
            <h2 style="color: #94a3b8;">Strategic Venture Control Hub</h2>
            <p style="color: #64748b;">Analyze <b>{idea if idea else 'your idea'}</b> in <b>{location if location else 'any location'}</b>.</p>
        </div>
    """, unsafe_allow_html=True)
