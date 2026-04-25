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

Create a detailed and location-specific business report.

Business Idea: {idea}
Location: {location}
Budget: {budget}

While analyzing, consider:
- Local demand in the given location
- Competition in that area
- Customer preferences and culture
- Pricing suitability
- Feasibility based on local conditions

IMPORTANT:
- Provide an approximate number of competitors (as a range, e.g., 10–20)
- Clearly mention that this is an estimate, not exact data

Include:

1. Executive Summary
2. Demand Analysis (location-specific)
3. Competition Analysis (include estimated competitor count)
4. SWOT Analysis
5. Risk Analysis
6. Budget Feasibility
7. Final Verdict (GO / NO-GO)
8. Score (0-100)

Make it realistic, practical, and tailored to the location.
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            report = response.choices[0].message.content

            st.write("## 🤖 AI Business Report")
            st.write(report)

        except Exception as e:
            st.error(f"Failed to generate report: {e}")
        
