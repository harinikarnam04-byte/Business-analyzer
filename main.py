import os
import streamlit as st
from groq import Groq
import pandas as pd

# Initialize Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Page config
st.set_page_config(page_title="AI Business Idea Analyzer", layout="wide")

# Title
st.title("🚀 Realistic Business Idea Analyzer")
st.markdown("---")

# Layout with two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Project Details")
    idea = st.text_input("Business Idea (e.g., Organic Cafe)")
    location = st.text_input("Location (e.g., Jayanagar, Bangalore)")
    budget = st.number_input("Total Budget (in ₹)", min_value=0, value=500000, step=50000)

with col2:
    st.subheader("📊 Typical Budget Breakdown")
    # Adding a visual pie chart for budget estimation
    chart_data = pd.DataFrame({
        "Category": ["Rent & Deposit", "Inventory/Stock", "Marketing", "Working Capital", "Licensing/Legal"],
        "Percentage": [40, 25, 15, 15, 5]
    })
    st.write("Average startup cost distribution:")
    st.pie_chart(chart_data, x="Category", y="Percentage")

# Button
if st.button("Generate Honest Analysis"):
    if not idea or not location or not budget:
        st.warning("Please fill all fields to get a realistic report.")
    else:
        with st.spinner("Analyzing market risks and competition..."):
            # The prompt is now much stricter to force "honesty"
            prompt = f"""
            You are a skeptical, high-stakes Venture Capitalist and Business Consultant. 
            Be brutally honest and realistic. Do not sugarcoat the challenges.

            Business Idea: {idea}
            Location: {location}
            Budget: ₹{budget}

            Analyze the feasibility with a focus on:
            1. Saturated Markets: If the location (like Bangalore) already has many such businesses, highlight the "Red Ocean" danger.
            2. Budget Gaps: If the budget is too low for the idea, state clearly why it might fail.
            3. Hidden Risks: Regulatory issues, local labor problems, or shifting consumer trends.

            Structure your response as follows:
            - **Honest Executive Summary** (Why this might fail vs why it might work)
            - **Market Reality Check** (Competition range in {location})
            - **SWOT Analysis** (Be heavy on Weaknesses and Threats)
            - **Budget Red Flags** (Is ₹{budget} actually enough?)
            - **Success Metrics** (Probability of success %, Estimated months to break even)
            - **Final Verdict** (STRICT: Choose either GO, CAUTION, or NO-GO)
            - **Total Score** (0-100)
            """

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )

                report = response.choices[0].message.content

                st.markdown("---")
                st.header("🤖 The Consultant's Reality Report")
                
                # Display the report
                st.markdown(report)
                
                st.success("Analysis Complete. Check the 'Final Verdict' for the honest truth!")

            except Exception as e:
                st.error(f"Failed to generate report: {e}")

st.markdown("---")
st.caption("Note: This tool uses AI to provide estimates. Always conduct ground-level market research before investing.")
