import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Page configuration
st.set_page_config(
    page_title="Pro Business Analyzer",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for professional metric cards (Fixed for Dark Mode - No solid white)
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05); 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Professional Business Idea Analyzer")
st.markdown("---")

# Sidebar / Input Section
with st.sidebar:
    st.header("📋 Input Parameters")
    idea = st.text_input("Business Concept", placeholder="e.g., Luxury Pet Spa")
    location = st.text_input("Target Location", placeholder="e.g., Jayanagar, Bangalore")
    budget = st.number_input("Available Capital (₹)", min_value=0, value=500000, step=50000)
    
    st.info("The AI acts as a skeptical Venture Capitalist to ensure honest, high-stakes feedback.")
    analyze_btn = st.button("Generate Reality Report", use_container_width=True)

# Main Dashboard Area
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("💡 Analysis Overview")
    if not idea:
        st.write("Enter your business idea in the sidebar to begin.")
    else:
        st.markdown(f"**Analyzing:** {idea}")
        st.markdown(f"**Market:** {location}")

with col_right:
    st.subheader("📊 Standard Budget Allocation")
    budget_df = pd.DataFrame({
        "Category": ["Rent & Setup", "Inventory", "Marketing", "Cash Reserve", "Legal/Ops"],
        "Percentage": [35, 25, 20, 15, 5]
    })
    
    fig = px.pie(
        budget_df, 
        values='Percentage', 
        names='Category', 
        hole=0.5, 
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# Logic Execution
if analyze_btn:
    if not idea or not location or not budget:
        st.error("Missing fields! Please provide Idea, Location, and Budget.")
    else:
        # VERIFIED INDENTATION: 4 spaces for every line inside the with block
        with st.spinner("Crunching market data and identifying risks..."):
            prompt = f"""
            You are a brutal, skeptical Business Consultant and VC. 
            Analyze: {idea} in {location} with budget ₹{budget}.
            DO NOT be optimistic. Be critical and honest.
            
            Structure the response exactly as follows:
            1. EXECUTIVE SUMMARY (Feasibility at this budget)
            2. COMPETITION (Estimate number of similar shops in {location})
            3. BUDGET REALITY CHECK (Is ₹{budget} truly enough for {location}?)
            4. WHY THIS MIGHT FAIL (Specific local risks)
            5. FINAL VERDICT (GO / CAUTION / NO-GO)
            6. SCORE (0-100)
            """

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                report_content = response.choices[0].message.content

                st.markdown("---")
                st.header("🤖 Consultant's Final Report")

                # Metrics Row
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Risk Level", "Critical Assessment", delta="Honest View")
                with m2:
                    st.metric("Budget Status", f"₹{budget}", delta="Check Gap Analysis", delta_color="inverse")
                with m3:
                    st.metric("Market Type", "Red Ocean", help="Highly competitive area")

                st.markdown("### 📝 Detailed Breakdown")
                st.info(report_content)

            except Exception as e:
                st.error(f"Error communicating with AI: {e}")

st.markdown("---")
st.caption("Developed for MBA Business Analytics Portfolio | RVIM 2026")
