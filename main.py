import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="BizAI | Strategic Pro", page_icon="💎", layout="wide")

# --- UI SETTINGS & CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    [data-testid="stMetric"] { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 20px; }
    .main-title { background: -webkit-linear-gradient(#38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.8rem; font-weight: 800; text-align: center; }
    .pivot-card { background: rgba(129, 140, 248, 0.1); border-radius: 10px; padding: 15px; border: 1px dashed #818cf8; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. MULTI-LANGUAGE TOGGLE ---
with st.sidebar:
    lang = st.radio("🌐 App Language", ["English", "ಕನ್ನಡ (Kannada)", "हिंदी (Hindi)"], horizontal=True)
    st.markdown("---")

st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.markdown("### 🛠 Strategy Configuration")
    with st.form("pro_form"):
        idea = st.text_input("Concept Name", placeholder="e.g. Organic Rooftop Cafe")
        location = st.text_input("Target Area", placeholder="e.g. Jayanagar")
        budget = st.number_input("Seed Capital (₹)", min_value=10000, value=1000000)
        audience = st.text_input("Target Audience", placeholder="e.g. Health-conscious youth")
        
        # --- 3. SENSITIVITY ANALYSIS (Inflation/Risk Slider) ---
        st.markdown("#### 📊 Market Sensitivity")
        market_stress = st.slider("Market Stress Level (Inflation/Risk)", 0, 100, 20)
        
        analyze_btn = st.form_submit_button("Launch 360° Analysis", use_container_width=True)
    st.caption("RVIM MBA Portfolio | 2026")

if analyze_btn:
    if not idea or not location:
        st.warning("Please provide a Concept and Location.")
    else:
        # Adjustment logic for Sensitivity Analysis
        adjusted_budget = budget * (1 - (market_stress / 100))
        
        with st.spinner("🤖 Analyzing pivots, language, and market stress..."):
            # --- 1. PIVOT ASSISTANT PROMPT ---
            prompt = f"""
            Analyze '{idea}' in '{location}' with budget ₹{budget}.
            Target Audience: {audience}. Market Stress: {market_stress}%. Language: {lang}.
            
            Provide:
            1. SWOT ANALYSIS.
            2. SUCCESS PROBABILITY (Consider {market_stress}% stress).
            3. PIVOT ASSISTANT: Suggest 2 alternative 'Pivot' ideas if this one is too risky.
            4. ENTREPRENEUR INSPIRATION: A successful founder in this field.
            5. VERDICT in {lang}.
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                report = response.choices[0].message.content

                # Dashboard Row
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric("Safe Budget", f"₹{int(adjusted_budget):,}", delta=f"-{market_stress}% Risk", delta_color="inverse")
                with m2:
                    st.metric("Market Context", location)
                with m3:
                    st.metric("Language", lang.split()[0])
                with m4:
                    st.metric("Survival", "Medium-High")

                st.markdown("---")
                
                col_left, col_right = st.columns([1.5, 1])
                with col_left:
                    st.markdown(f"### 📋 Strategic Report ({lang})")
                    st.info(report)
                
                with col_right:
                    st.markdown("#### 📊 Adjusted CapEx Split")
                    # Sensitivity analysis affects the 'Reserve' fund
                    reserve_pct = 0.10 + (market_stress / 500)
                    df = pd.DataFrame({
                        "Dept": ["Rent", "Stock", "Marketing", "Risk Reserve"],
                        "Amt": [0.4, 0.3, 0.3 - reserve_pct, reserve_pct]
                    })
                    fig = px.pie(df, values='Amt', names='Dept', hole=0.5, color_discrete_sequence=px.colors.sequential.Plotly3)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), margin=dict(t=0,b=0,l=0,r=0))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown('<div class="pivot-card"><b>💡 MBA Tip:</b> High stress requires a larger Risk Reserve. See the adjusted chart above.</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.markdown("<div style='text-align: center; padding: 50px;'><h3>Ready for Strategic Deep-Dive?</h3><p>Configure Stress Levels and Language in the sidebar.</p></div>", unsafe_allow_html=True)
    
