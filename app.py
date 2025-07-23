import streamlit as st
import requests
import pandas as pd


API_URL = "http://localhost:8000/query"

st.set_page_config(page_title="E-Commerce QA AI", layout="wide")
st.title("📊 E-Commerce QA AI - Visual Dashboard")
st.markdown("Ask a question (e.g., 'What is total sales?')")

user_question = st.text_input("Enter your question:")

if st.button("Generate Answer / Visualization"):
    if not user_question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Processing..."):
            try:
                response = requests.post(API_URL, json={"question": user_question})
                if response.status_code == 200:
                    data = response.json()

                    # Display answer table if available
                    records = data.get("answer", [])
                    if records:
                        st.subheader("Results")
                        st.dataframe(pd.DataFrame(records))

                    
                    visual = data.get("visual", None)
                    if isinstance(visual, dict) and "image_base64" in visual:
                        st.subheader("Visualization")
                        st.image("data:image/png;base64," + visual["image_base64"])
                    elif isinstance(visual, str):
                        
                        if visual.startswith("data:image/png;base64,"):
                            st.subheader("Visualization")
                            st.image(visual)
                        else:
                            st.info(visual)
                    else:
                        st.info("No chart available.")
                else:
                    st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error contacting API: {e}")