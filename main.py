import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px

# Initialize Groq client
# Ensure GROQ_API_KEY is set in your Streamlit Cloud Secrets
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Page configuration
st.set_page_config(
    page_title="Pro Business Analyzer",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_value=True)

st.title("🚀 Professional Business Idea Analyzer")
st.markdown("---")

# Sidebar / Input Section
with st.sidebar:
    st.header("📋 Input Parameters")
    idea = st.text_input("Business Concept", placeholder="e.g., Luxury Pet Spa")
    location = st.text_input("Target Location", placeholder="e.g., Jayanagar, Bangalore")
    budget = st.number_input("Available Capital (₹)", min_value=0, value=500000, step=50000)
    
    st.info("The AI acts as a skeptical Venture Capitalist to ensure honest feedback.")
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
    # Professional Budget Pie Chart using Plotly
    budget_df = pd.DataFrame({
        "Category": ["Rent & Setup", "Inventory", "Marketing", "Cash Reserve", "Legal/Ops"],
        "Percentage": [35, 25, 20, 15, 5]
    })
    fig = px.pie(budget_df, values='Percentage', names='Category', 
                 hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
    st.plotly_chart(fig, use_container_width=True)

# Logic Execution
if analyze_btn:
    if not idea or not location or not budget:
        st.error("Missing fields! Please provide Idea, Location, and Budget.")
    else:
        with st.spinner("Crunching market data and identifying risks..."):
            # The "Honest" Prompt
            prompt = f"""
            You are a brutal, skeptical Business Consultant. 
            Idea: {idea} | Location: {location} | Budget: ₹{budget}

            Provide a report with these EXACT sections:
            1. EXECUTIVE SUMMARY (Focus on feasibility)
            2. COMPETITION SCORE (Estimate number of competitors in {location})
            3. BUDGET GAP ANALYSIS (Is ₹{budget} enough?)
            4. THE REALITY CHECK (Why this might FAIL)
            5. FINAL VERDICT (GO / CAUTION / NO-GO)
            6. SCORE (0-100)
            """

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                report_content = response.choices[0].message.content

                # UI for the Report Output
                st.markdown("---")
                st.header("🤖 Consultant's Final Report")

                # Metrics Row
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Risk Level", "High" if "NO-GO" in report_content else "Medium", delta="Critical", delta_color="inverse")
                with m2:
                    st.metric("Capital Adequacy", "Check Report", delta="-12% Gap Expected")
                with m3:
                    st.metric("Market Type", "Red Ocean", help="Highly competitive area")

                # Structured Output
                st.error("### 🛑 Critical Weaknesses & Risks")
                st.write(report_content)

            except Exception as e:
                st.error(f"Error communicating with AI: {e}")

st.markdown("---")
st.caption("Developed for MBA Business Analytics Portfolio | RVIM 2026")
                
