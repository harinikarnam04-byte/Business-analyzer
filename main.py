import os
import streamlit as st
from groq import Groq
import matplotlib.pyplot as plt

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="AI Business Idea Analyzer")

st.title("🚀 AI Business Idea Analyzer")

idea = st.text_input("Business Idea")
location = st.text_input("Location")
budget = st.text_input("Budget")

if st.button("Analyze"):
    if not idea or not location or not budget:
        st.warning("Please fill all fields")
    else:
        prompt = f"""
You are a highly practical and realistic startup consultant.

Business Idea: {idea}
Location: {location}
Budget: {budget}

IMPORTANT RULES:
- If location is small/unknown (like tier-3 towns), assume realistic local conditions
- DO NOT say "unable to analyze"
- Give best possible estimation based on typical Indian tier-2/tier-3 markets
- Avoid being overly optimistic — be balanced and slightly conservative
- Highlight real risks clearly

Include:

1. Executive Summary
2. Demand Analysis (based on local population type)
3. Competition Analysis (estimate range)
4. SWOT Analysis
5. Risk Analysis
6. Budget Feasibility

7. 📊 Success Metrics:
   - Success Rate (%)
   - Time to Success

8. Final Verdict:
   - GO / NO-GO
   - Clear reasoning

9. Top 3 Critical Success Factors

10. Score (0-100)

Make it realistic, honest, and practical.
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )

            report = response.choices[0].message.content

            st.write("## 🤖 AI Business Report")
            st.write(report)

            # --- SIMPLE PIE CHART ---
            st.write("## 📊 Visual Risk Analysis")

            # Example fixed values (can later extract from AI)
            success = 70
            risk = 30

            labels = ['Success Probability', 'Risk']
            sizes = [success, risk]

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%')
            ax.axis('equal')

            st.pyplot(fig)

        except Exception as e:
            st.error(f"Failed to generate report: {e}")
