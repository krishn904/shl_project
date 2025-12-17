import streamlit as st
import requests

# Set page title and icon
st.set_page_config(page_title="SHL Assessment Finder", page_icon="🔍")

st.title("🎯 SHL Assessment Recommender")
st.write("Enter a job description or skill query to find the best SHL assessments.")

# API URL - REPLACE THIS WITH YOUR ACTUAL RENDER URL
# Ensure it ends with /recommend
API_URL = "https://shl-project-aooj.onrender.com"

# User Input Area
query = st.text_area("What role or skills are you hiring for?", 
                     placeholder="e.g., Hiring for a Python developer with SQL skills...")

if st.button("Find Assessments"):
    if query:
        with st.spinner('Searching for matches...'):
            try:
                # Call your Render API
                response = requests.post(API_URL, json={"query": query})
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("recommended_assessments", [])
                    
                    if results:
                        st.success(f"Found {len(results)} recommendations:")
                        for item in results:
                            with st.expander(f"✅ {item['name']}"):
                                st.write(f"**Description:** {item['description']}")
                                st.write(f"**Duration:** {item['duration']} mins")
                                st.write(f"**Type:** {', '.join(item['test_type'])}")
                                st.link_button("View Assessment", item['url'])
                    else:
                        st.warning("No specific assessments found for this query.")
                else:
                    st.error(f"API Error: Received status code {response.status_code}")
            except Exception as e:
                st.error(f"Failed to connect to the API. Make sure your Render URL is correct. Error: {e}")
    else:
        st.info("Please enter a query before clicking the button.")