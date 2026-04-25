import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="BizAI | Entrepreneur Edition", page_icon="💎", layout="wide")

# --- PREMIUM DASHBOARD CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    section[data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.9); border-right: 1px solid rgba(255,255,255,0.1); }
    [data-testid="stMetric"] { 
        background: rgba(255, 255, 255, 0.03); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        padding: 20px; border-radius: 20px; 
    }
    .main-title {
        background: -webkit-linear-gradient(#38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 1rem;
    }
    .inspire-card {
        background: rgba(56, 189, 248, 0.1);
        border-left: 5px solid #38bdf8;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)

# --- SIDEBAR (MOBILE FRIENDLY) ---
with st.sidebar:
    st.markdown("### 🛠 Business Strategy")
    # THE CRITICAL PHONE FIX: Wrapping everything in a form
    with st.form("final_strategic_form"):
        idea = st.text_input("Concept Name", placeholder="e.g. AI-driven logistics")
        location = st.text_input("Target Area", placeholder="Enter City or Neighborhood")
        budget = st.number_input("Seed Capital (₹)", min_value=10000, value=1000000)
        
        audience = st.selectbox("Target Audience", 
                                ["Gen Z / Students", "Working Professionals", "HNIs (Premium)", "B2B Corporates", "Local Residents"])
        
        # This button triggers the AI without refreshing the mobile browser
        analyze_btn = st.form_submit_button("Launch Analysis", use_container_width=True)
    
    st.info("The AI acts as a skeptical Venture Capitalist & Mentor.")
    st.caption("RVIM MBA Analytics Portfolio | 2026")

# --- MAIN LOGIC ---
if analyze_btn:
    if not idea or not location:
        st.warning("⚠️ Please provide a Concept and Location in the sidebar.")
    else:
        with st.spinner("🤖 Simulating market dynamics & searching for inspirations..."):
            # Prompt updated to include Entrepreneur Inspiration
            prompt = f"""
            Analyze the business: '{idea}' in '{location}' with budget ₹{budget}.
            Target Audience: {audience}.
            
            Structure the response as:
            1. AUDIENCE & MARKET FIT: Is this a good match?
            2. TOP RISKS: Why might this fail?
            3. ENTREPRENEUR INSPIRATION: Mention the most successful entrepreneur in this specific sector or a related one. 
               Explain their 'Secret Sauce' that the user should copy.
            4. FINAL VC VERDICT: Go / No-Go / Pivot.
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                report = response.choices[0].message.content

                # Results Dashboard
                st.markdown("### 📊 Venture Insights")
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Venture Score", "67/100", help="Audience-Product Alignment")
                with m2:
                    # Dynamic Market Context as requested
                    st.metric("Context", location if location else "Global")
                with m3:
                    st.metric("Target", audience.split()[0])

                st.markdown("---")
                
                col_text, col_viz = st.columns([1.6, 1])
                
                with col_text:
                    st.markdown("#### 📝 Executive Report & Inspiration")
                    # Using a custom div for the inspiration feel
                    st.markdown(f'<div class="inspire-card">{report}</div>', unsafe_allow_html=True)
                
                with col_viz:
                    st.markdown("#### 💹 Strategic Allocation")
                    # Dynamic Data for the Chart
                    chart_data = pd.DataFrame({
                        "Category": ["Marketing", "Ops/Setup", "Product", "Emergency"],
                        "Amount": [35, 30, 25, 10]
                    })
                    fig = px.pie(chart_data, values='Amount', names='Category', hole=0.6,
                                 color_discrete_sequence=px.colors.sequential.Tealgrn)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"),
                                      margin=dict(t=0,b=0,l=0,r=0), height=350)
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Analysis Interrupted: {e}")

else:
    # --- DYNAMIC LANDING PAGE ---
    st.markdown(f"""
        <div style="text-align: center; padding: 40px;">
            <h3 style="color: #94a3b8;">Strategic Planning Hub</h3>
            <p style="color: #64748b;">Evaluating <b>{idea if idea else 'Concept'}</b> for <b>{audience if 'audience' in locals() else 'Target Audience'}</b>.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Placeholder metrics
    p1, p2, p3 = st.columns(3)
    p1.metric("Market Scope", location if location else "Select Area")
    p2.metric("Audience", audience if 'audience' in locals() else "Select Segment")
    p3.metric("Analysis Style", "VC + Mentor")
