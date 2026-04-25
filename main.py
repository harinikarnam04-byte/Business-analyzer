import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Page configuration
st.set_page_config(
    page_title="BizAI | Venture Master",
    page_icon="💎",
    layout="wide"
)

# --- PREMIUM DASHBOARD CSS ---
st.markdown("""
    <style>
    /* Gradient Background */
    .stApp { 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
        color: #f8fafc; 
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { 
        background-color: rgba(15, 23, 42, 0.9); 
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Glassmorphism Metric Cards */
    [data-testid="stMetric"] { 
        background: rgba(255, 255, 255, 0.03); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        padding: 20px; 
        border-radius: 20px; 
        backdrop-filter: blur(10px);
    }

    /* Custom Report Box */
    .report-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #818cf8;
        line-height: 1.6;
    }

    /* Gradient Title */
    .main-title {
        background: -webkit-linear-gradient(#38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; 
        font-weight: 800; 
        text-align: center;
        margin-bottom: 20px;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        border: none;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)

# --- SIDEBAR (MOBILE-STABLE FORM) ---
with st.sidebar:
    st.markdown("### 🛠 Business Configuration")
    # THE PHONE FIX: Wrapping everything in a form prevents mobile glitches
    with st.form("master_venture_form"):
        idea = st.text_input("Concept Name", placeholder="e.g. AI-driven Logistics")
        location = st.text_input("Target Area", placeholder="e.g. Jayanagar, Bangalore")
        budget = st.number_input("Seed Capital (₹)", min_value=10000, value=1000000, step=50000)
        
        # Open-ended Target Audience as requested
        audience = st.text_input("Target Audience", placeholder="e.g. Tech-savvy Gen Z")
        
        exp = st.selectbox("Founder Experience", ["Beginner", "Intermediate", "Expert"])
        
        # Submit button triggers analysis without refreshing browser
        analyze_btn = st.form_submit_button("Launch 360° Analysis", use_container_width=True)
    
    st.markdown("---")
    st.info("The AI provides a brutally honest VC assessment and identifies inspirational founders.")
    st.caption("Developed for MBA Analytics | RVIM 2026")

# --- MAIN ANALYSIS LOGIC ---
if analyze_btn:
    if not idea or not location:
        st.warning("⚠️ Please provide at least a Business Concept and a Location.")
    else:
        with st.spinner("🔄 Running simulations and market-fit analysis..."):
            # Master Prompt: Combining SWOT, Success Rate, Time, Risks, and Inspiration
            prompt = f"""
            Analyze the business idea '{idea}' in '{location}' with a budget of ₹{budget}.
            Target Audience: {audience if audience else 'General Public'}.
            Experience Level: {exp}.
            
            Provide a professional, brutally honest review structured as follows:
            1. FULL SWOT ANALYSIS (Strengths, Weaknesses, Opportunities, Threats).
            2. TOP RISKS & SUCCESS PROBABILITY (Estimate a % based on industry data).
            3. ESTIMATED TIME TO LAUNCH (Weeks/Months for MVP).
            4. ENTREPRENEUR INSPIRATION: Identify the most successful entrepreneur in this sector. 
               Explain their 'Secret Sauce' and what this user can learn from them.
            5. FINAL VERDICT: Go / No-Go / Pivot.
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                report_content = response.choices[0].message.content

                # Results Dashboard
                st.markdown("### 📈 Venture Reality Dashboard")
                
                # Metrics Row
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric("Risk Score", "Critical", delta="Honest View")
                with m2:
                    st.metric("Market Context", location if location else "Global")
                with m3:
                    st.metric("Time to MVP", "4-6 Months", help="Estimated Setup Phase")
                with m4:
                    st.metric("Runway", "9-12 Months", delta="Post-Setup")

                st.markdown("---")
                
                # Detailed Analysis Layout
                col_left, col_right = st.columns([1.5, 1])
                
                with col_left:
                    st.markdown("#### 📑 Strategic Assessment")
                    st.markdown(f'<div class="report-box">{report_content}</div>', unsafe_allow_html=True)
                
                with col_right:
                    st.markdown("#### 📊 Operations & Capex Split")
                    # Detailed breakdown logic
                    chart_data = pd.DataFrame({
                        "Department": ["Rent (Inc. Deposit)", "Inventory/Hardware", "Digital Marketing", "Legal & Permits", "Contingency Fund"],
                        "Allocation": [budget*0.35, budget*0.30, budget*0.20, budget*0.05, budget*0.10]
                    })
                    fig = px.pie(chart_data, values='Allocation', names='Department', hole=0.5,
                                 color_discrete_sequence=px.colors.sequential.Agsunset)
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', 
                        font=dict(color="white"),
                        showlegend=True,
                        margin=dict(t=0,b=0,l=0,r=0),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Strategic Badges
                    st.info(f"📍 Location focus: {location}")
                    st.success(f"🎯 Targeting: {audience if audience else 'Mass Market'}")

            except Exception as e:
                st.error(f"Analysis Error: {e}")

else:
    # --- LANDING PAGE ---
    st.markdown(f"""
        <div style="text-align: center; padding: 60px;">
            <h2 style="color: #94a3b8;">Strategic Venture Control Hub</h2>
            <p style="color: #64748b;">Ready to analyze <b>{idea if idea else 'your next big move'}</b> for 
            <b>{location if location else 'any market'}</b>.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Placeholder Display
    c1, c2, c3 = st.columns(3)
    c1.metric("Status", "Engine Ready")
    c2.metric("Market Context", location if location else "Pending")
    c3.metric("Analysis Style", "VC-Brutal")
