import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Page configuration - Using 'centered' for much better mobile response
st.set_page_config(
    page_title="Pro Business Analyzer",
    page_icon="🚀",
    layout="centered"
)

# Custom CSS for dark/light mode compatibility
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05); 
        padding: 15px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Business Idea Analyzer")
st.markdown("---")

# Sidebar with Form Wrap (Prevents mobile refresh issues)
with st.sidebar:
    st.header("📋 Input Parameters")
    with st.form("mobile_safe_form"):
        idea = st.text_input("Business Concept", placeholder="e.g., Pet Spa")
        location = st.text_input("Target Location", placeholder="e.g., Jayanagar")
        budget = st.number_input("Available Capital (₹)", min_value=0, value=500000, step=50000)
        
        # Use_container_width ensures the button fits any screen size
        analyze_btn = st.form_submit_button("Generate Reality Report", use_container_width=True)
    
    st.info("The AI provides a brutally honest VC-style assessment.")

# Logic Execution
if analyze_btn:
    if not idea or not location or not budget:
        st.error("Please fill in all details in the sidebar form.")
    else:
        # Indentation verified: 8 spaces here
        with st.spinner("Analyzing market risks..."):
            prompt = f"Analyze: {idea} in {location} with budget ₹{budget}. Be a skeptical consultant. Give a numbered report with risks, competition, and a final verdict."

            try:
                # API Call logic
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                report_text = response.choices[0].message.content

                # Results Layout
                st.markdown("---")
                st.header("🤖 Consultant's Final Report")

                # Metrics stack automatically on mobile in 'centered' layout
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Risk Level", "Critical", delta="Honest View")
                with m2:
                    st.metric("Budget", f"₹{budget}", delta="Assessment")
                with m3:
                    st.metric("Market", "Red Ocean")

                st.markdown("### 📝 Detailed Breakdown")
                st.info(report_text)

            except Exception as e:
                st.error(f"Connection Error: {e}")

# Default view if button hasn't been clicked yet
else:
    st.subheader("💡 Ready to Analyze")
    st.write("Open the sidebar (arrow on top-left for mobile) and enter your idea.")
    
    # Static visual for empty state
    dummy_df = pd.DataFrame({
        "Task": ["Rent", "Stock", "Marketing", "Reserve"],
        "Value": [40, 30, 20, 10]
    })
    fig = px.pie(dummy_df, values='Value', names='Task', hole=0.4)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Developed for MBA Portfolio | RVIM 2026")
