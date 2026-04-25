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

Create a highly practical and location-specific business report.

Business Idea: {idea}
Location: {location}
Budget: {budget}

While analyzing, consider:
- Local demand
- Competition in the area
- Customer preferences and culture
- Pricing suitability
- Feasibility based on local conditions

IMPORTANT:
- Provide an approximate number of competitors (as a range, e.g., 10–20)
- Clearly mention it is an estimate
- Give a realistic Success Rate (%) based on market conditions
- Estimate Time to Success (e.g., 6 months, 1 year, 2 years)

Include:

1. Executive Summary
2. Demand Analysis (location-specific)
3. Competition Analysis (with estimated competitor count)
4. SWOT Analysis
5. Risk Analysis
6. Budget Feasibility

7. 📊 Success Metrics:
   - Success Rate (%)
   - Expected Time to Success

8. Final Verdict:
   - Clear decision (GO / NO-GO)
   - 2–3 strong actionable suggestions to improve success chances

9. Score (0–100)

Make it realistic, practical, and actionable like a real consultant.
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
