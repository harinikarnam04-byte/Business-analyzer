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

# Custom CSS for a professional look (FIXED LINE 23)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #eee;
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
    # Professional Budget Pie Chart using Plotly
    budget_df = pd.DataFrame({
        "Category": ["Rent & Setup", "Inventory", "Marketing", "Cash Reserve", "Legal/Ops"],
        "Percentage": [35, 25, 20, 15, 5]
    })
    fig = px.pie(budget_df, values='Percentage', names='Category',
