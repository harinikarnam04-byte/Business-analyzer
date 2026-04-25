import os
import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="BizAI Venture Master", page_icon="💎", layout="wide")

# --- MOBILE-FIRST STRATEGIC UI ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    
    /* Strategy Block Styling */
    .strategy-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #38bdf8;
        padding: 22px;
        border-radius: 15px;
        margin: 15px 0px;
        line-height: 1.6;
    }

    .main-title {
        background: -webkit-linear-gradient(#38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 20px;
    }

    /* Mobile-Ready Form Button */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 3.5em;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        border: none; color: white; font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0px 4px 15px rgba(56, 189, 248, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)

# --- SIDEBAR (THE PHONE FIX RETAINED) ---
with st.sidebar:
    st.markdown("### 🌐 Localization")
    lang = st.radio("Output Language", ["English", "ಕನ್ನಡ", "हिंदी"], horizontal=True)
    st.markdown("---")
    
    with st.form("ultimate_strategy_form"):
        st.markdown("### 🛠 Project Configuration")
        idea = st.text_input("Business Concept", placeholder="e.g. Smart Logistics")
        location = st.text_input("Target Area", placeholder="e.g. Jayanagar")
        audience = st.text_input("Target Audience", placeholder="e.g. Local retailers")
        exp = st.selectbox("Founder Experience", ["Beginner", "Intermediate", "Expert"])
        
        # This button ensures mobile users don't lose progress
        analyze_btn = st.form_submit_button("Generate 360° Strategy", use_container_width=True)
    
    st.caption("Strategic Analytics Portfolio | RVIM")

# --- ANALYSIS ENGINE ---
if analyze_btn:
    if not idea or not location:
        st.warning("⚠️ Please provide at least the Business Concept and Location.")
    else:
        with st.spinner("🤖 Mapping SWOT, Funding Paths & Inspirations..."):
            # PROMPT: Includes SWOT, Inspiration, Risks, and NEW Funding focus
            prompt = f"""
            Analyze the venture '{idea}' in '{location}'.
            Audience: {audience if audience else 'General market'}. Experience: {exp}.
            
            Provide a professional and honest report covering:
            1. FULL SWOT ANALYSIS: A detailed Strengths, Weaknesses, Opportunities, and Threats breakdown.
            2. MARKET REALITY: Current viability and risks in {location}.
            3. FUNDING OPPORTUNITIES: Suggest specific ways to raise capital (e.g., Angel Investors, Venture Capital, Crowdfunding, or Incubators) relevant to this sector.
            4. FOUNDER INSPIRATION: Mention a successful entrepreneur in this field and their "Secret Sauce" or strategy.
            5. FINAL VERDICT: A clear Go / No-Go / Pivot recommendation in {lang}.
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                report = response.choices[0].message.content

                # Results Dashboard
                st.markdown("### 📋 Executive Feasibility Report")
                
                # Single vertical card for maximum mobile readability
                st.markdown(f'<div class="strategy-card">{report}</div>', unsafe_allow_html=True)
                
                st.success(f"Strategy delivered in {lang} • Analysis level: {exp}")

            except Exception as e:
                st.error(f"Error: {e}")
else:
    # Landing Page State
    st.markdown(f"""
        <div style="text-align: center; padding: 50px; opacity: 0.7;">
            <h3>Strategic Planning Hub</h3>
            <p>Enter your venture parameters to see a 360° breakdown of SWOT, Funding, and Market Risk.</p>
        </div>
    """, unsafe_allow_html=True)
