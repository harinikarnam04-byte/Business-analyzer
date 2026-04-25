import os
import streamlit as st
from groq import Groq

# Initialize Groq client using environment variable
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Page config
st.set_page_config(page_title="AI Business Idea Analyzer")

# Title
st.title("🚀 AI Business Idea Analyzer")

# Inputs
idea = st.text_input("Business Idea")
location = st.text_input("Location")
budget = st.text_input("Budget")

# Button
if st.button("Analyze"):
    if not idea or not location or not budget:
        st.warning("Please fill all fields")
    else:
        prompt = f"""
You are a world-class startup business consultant.

Create a detailed business report in a structured format:

Business Idea: {idea}
Location: {location}
Budget: {budget}

Include the following sections:

1. Executive Summary
2. Demand Analysis
3. Competition Analysis
4. SWOT Analysis
5. Risk Analysis
6. Budget Feasibility
7. Final Verdict (GO / NO-GO)
8. Score (0-100)

Make it realistic, practical, and actionable.
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            report = response.choices[0].message.content

            st.write("## 🤖 AI Business Report")
            st.write(report)

        except Exception as e:
            st.error(f"Failed to generate report: {e}")
