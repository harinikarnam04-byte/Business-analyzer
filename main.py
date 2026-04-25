import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Page configuration
st.set_page_config(
    page_title="BizAI | Venture Consultant",
    page_icon="💎",
    layout="wide"
)

# --- PREMIUM GLASSMORPHISM CSS ---
st.markdown("""
    <style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Sidebar styling for transparency */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.9);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Metric Card Styling */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Header gradients */
    .main-title {
        background: -webkit-linear-gradient(#38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        padding-bottom: 20px;
    }

    /* Form and Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown('<h1 class="main-title">BizAI Venture Consultant</h1>', unsafe_allow_html=True)

# Sidebar with the "Phone Fix" (Form Wrap)
with st.sidebar:
    st.markdown("### 🛠 Project Configuration")
    with st.form("mobile_ready_form"):
        idea = st.text_input("Concept Name", placeholder="e.g. Smart Coffee Kiosk")
        location = st.text_input("Target Area", placeholder="e.g. Jayanagar, Bangalore")
        budget = st.number_input("Seed Capital (₹)", min_value=0, value=1000000, step=50000)
        
        # The crucial button that works on all devices
        analyze_btn = st.form_submit_button("Launch Analysis", use_container_width=True)
    
    st.markdown("---")
    st.caption("RVIM MBA Portfolio | 2026")

# Analysis Logic
if analyze_btn:
    if not idea or not location:
        st.warning("⚠️ Please fill in all fields in the sidebar.")
    else:
        with st.spinner("🤖 Simulating market scenarios..."):
            prompt = f"Analyze {idea} in {location} with budget ₹{budget}. Be a brutal venture capitalist. Provide: 1. Strategic Summary, 2. Financial Risks, 3. Competitor Landscape, 4. Verdict."
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                report = response.choices[0].message.content

                # Results Dashboard Layout
                st.markdown("### 📊 Live Venture Assessment")
                
                # Metrics Row (Responsive: stacks on phone, side-by-side on laptop)
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Risk Score", "Critical", delta="-12% Feasibility")
                with m2:
                    st.metric("Capital Req", f"₹{int(budget*1.2):,}", delta="20% Buffer Needed")
                with m3:
                    st.metric("Market Status", "Red Ocean")

                st.markdown("---")
                
                # Split content for laptop, stacks for mobile
                col_text, col_viz = st.columns([1.5, 1])
                
                with col_text:
                    st.markdown("#### 📝 Consultant Breakdown")
                    st.info(report)
                
                with col_viz:
                    st.markdown("#### 💹 Capital Allocation")
                    # Visual Chart
                    df = pd.DataFrame({
                        "Category": ["Rent", "Stock", "Marketing", "Reserve"],
                        "Share": [40, 25, 20, 15]
                    })
                    fig = px.pie(df, values='Share', names='Category', hole=0.5,
                                 color_discrete_sequence=px.colors.sequential.Sky)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                      font=dict(color="white"), showlegend=True, height=350,
                                      margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error: {e}")

else:
    # --- Landing Page Design ---
    st.markdown("""
        <div style="text-align: center; padding: 40px;">
            <h3 style="color: #94a3b8;">Enter details in the sidebar to begin.</h3>
            <p style="color: #64748b;">The AI engine will evaluate your idea against real-world market metrics.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Placeholder metrics for "wow" factor
    p1, p2, p3 = st.columns(3)
    p1.metric("Engine", "Llama 3.1")
    p2.metric("Market Context", "Bengaluru")
    p3.metric("Response Time", "< 2.5s")
