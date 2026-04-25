import os
import streamlit as st
from groq import Groq
import pandas as pd
import plotly.express as px  # Professional charting library

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Page config
st.set_page_config(page_title="AI Business Idea Analyzer", layout="wide")

# Title
st.title("🚀 Realistic Business Idea Analyzer")
st.markdown("---")

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Project Details")
    idea = st.text_input("Business Idea")
    location = st.text_input("Location")
    budget = st.number_input("Total Budget (in ₹)", min_value=0, value=500000)

with col2:
    st.subheader("📊 Typical Budget Breakdown")
    # Data for the chart
    df = pd.DataFrame({
        "Category": ["Rent/Deposit", "Inventory", "Marketing", "Operations", "Legal"],
        "Amount": [40, 25, 15, 15, 5]
    })
    
    # Using Plotly for a more professional interactive Pie Chart
    fig = px.pie(df, values='Amount', names='Category', hole=0.4,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

# Button
if st.button("Generate Honest Analysis"):
    if not idea or not location or not budget:
        st.warning("Please fill all fields")
    else:
        with st.spinner("Analyzing market risks..."):
            prompt = f"""
            You are a skeptical business consultant. 
            Analyze this idea: {idea} in {location} with a budget of ₹{budget}.
            Be brutally honest. If the budget is too low for the location, say so.
            
            Provide:
            1. Market Satiation Check
            2. Real-world Competitor Estimate
            3. Detailed Risk Analysis
            4. Final Verdict: (GO / NO-GO)
            """
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown("### 🤖 The Reality Check")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
