import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

# Logic 1 Template
chat_template = ChatPromptTemplate(
    messages =[("system", """You are an intelligent and helpful AI travel assistant that helps users find the best travel options
                          between a given source and destination. You analyze various travel modes, including cabs, trains, buses,
                          and flights, and provide estimated costs, durations, and relevant insights. Your responses should be clear,
                          concise, and formatted for easy understanding. If real-time data is available, incorporate it; otherwise,
                          provide the best general estimates. Always ensure accuracy and helpfulness in your recommendations.
                          Always respond in **valid JSON format** with travel options.
                          Your response should be structured as a list of travel options, each containing:
                               - Travel mode (e.g., Flight, Train, Bus, Cab)
                               - Cost (in INR, prefixed with "₹")
                               - Duration (e.g., "5 hours")
                               - Brief details of the trip
                          Can include explanations upto 50 words, markdown formatting, or any extra text—only return valid JSON"""),
              ("human", "Find the best travel options from {source} to {destination}.")
              ]
)


# Logic 2 Model
f = open("/content/api.txt")
API_KEY = f.read()

chat_model = ChatGoogleGenerativeAI(google_api_key=API_KEY,
    model="gemini-2.0-flash")

# Logic 3 OutputParser
chat_parser = JsonOutputParser()

# Initializing the Langchain
chain = chat_template | chat_model | chat_parser

# Function to Get Travel Recommendations
def get_travel_recommendations(source, destination):
    response = chain.invoke({"source": source, "destination": destination})
    print("Raw AI Response:", response)
    return response


# Streamlit UI
st.set_page_config(page_title="AI Tour Planner", page_icon="🌎", layout="centered")
st.title("🌎 AI Tour Planner")
st.subheader("Find the best travel options for your trip!")

# User Inputs
col1, col2 = st.columns(2)

with col1:
    source = st.text_input("Enter Source Location", placeholder="Departure")

with col2:
    destination = st.text_input("Enter Destination Location", placeholder="Arrival")

# Process on Button Click
if st.button("Finding Best Travel Options", use_container_width=True):
    if source and destination:
        with st.spinner("Fetching travel recommendations..."):
            result = get_travel_recommendations(source, destination)

            
            if isinstance(result, list):
                st.write("### Recommended Travel Options:")

                cols = st.columns(len(result))
                

                for i, option in enumerate(result):
                    with cols[i]: 
                        st.markdown(f"### {option.get('Travel Mode', 'Unknown')}")
                        st.markdown(f"**Cost:** {option.get('Cost', 'N/A')}")
                        st.markdown(f"**Duration:** {option.get('Duration', 'Unknown')}")
                        st.info(option.get('Details', 'No details available'))
            else:
                st.error("Unexpected response format. Please try again.")
    else:
        st.warning("Please enter both source and destination.")

