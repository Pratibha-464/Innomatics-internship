import streamlit as st
import google.generativeai as genai
import pandas as pd

# Set up Google Gemini API
f = open("/content/api.txt")
API_KEY = f.read()
genai.configure(api_key=API_KEY)


system_prompt = """
    You are an AI code reviewer. Review the following code, specify any errors in it,
    and provide a revised version that fixes those errors.

    Your response should be structured as follows:
    **Errors Identified:**
    - Issue: [Error Type] - [Error Description]

    **Revised Code:**
    (Provide the corrected version of the code)
"""



# Streamlit Page Setup
st.set_page_config(page_title="AI Code Reviewer", layout="wide")

st.title("🧑‍💻 AI Code Reviewer")
st.write("📌 Submit your Python code and get an AI-generated analysis with fixes.")

# User Input Box
user_prompt = st.text_area("Enter your Python code below:", height=200)

# Button to Trigger Analysis
if st.button("🚀 Review Code"):
    if user_prompt.strip():
        st.success("Analyzing code... Please wait.")

        # Prepare Full Prompt for AI
        full_prompt = f"{system_prompt}\n\n```python\n{user_prompt}\n```"

        # Generate response from Gemini AI
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt)

        if response and response.text:
            # Split response into Errors and Revised Code
            sections = response.text.split("**Revised Code:**")
            errors_section = sections[0].replace("**Errors Identified:**", "").strip()
            revised_code = sections[1].strip() if len(sections) > 1 else "No fixes provided."

            # Convert Errors into a DataFrame
            error_data = []
            for line in errors_section.split("\n"):
                if line.startswith("- Issue: "):
                    parts = line.replace("- Issue: ", "").split(" - ")
                    if len(parts) == 2:
                        error_data.append({"Issue": parts[0], "Description": parts[1]})

            if error_data:
                df = pd.DataFrame(error_data)
                st.write("### Error Summary Table")
                st.dataframe(df)

            # Side-by-Side Code Comparison
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔍 Original Code")
                st.code(user_prompt, language="python")

            with col2:
                st.subheader("✅ Revised Code")
                st.code(revised_code, language="python")

        else:
            st.warning("⚠️ No response received from AI.")
    else:
        st.warning("⚠️ Please enter some Python code before reviewing.")

st.markdown("---")
st.write("🤖 Powered by **Google Gemini AI**")
