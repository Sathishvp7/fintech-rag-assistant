import streamlit as st
import requests

# --- Configuration ---
FASTAPI_URL = "http://127.0.0.1:8000/query"

# --- Streamlit UI ---
st.set_page_config(page_title="RBAC RAG POC", layout="wide")

st.title("RAG System with Role-Based Access Control (RBAC)")
st.write("""
This proof-of-concept demonstrates a RAG system that enforces access control based on user roles.
Select a role and ask a question to see how the system responds with filtered information.
""")

# --- User Inputs ---
st.sidebar.header("Query Controls")
user_role = st.sidebar.selectbox(
    "Select Your Role",
    ("c-level", "employee", "engineer", "hr", "finance", "marketing"),
    index=0
)

question = st.text_input(
    "Ask a question",
    placeholder="e.g., What is the policy on remote work?"
)

if st.button("Get Answer"):
    if not question:
        st.error("Please enter a question.")
    else:
        with st.spinner("Searching for an answer..."):
            try:
                # Prepare the request payload
                payload = {"question": question, "user_role": user_role}

                # Send request to FastAPI backend
                response = requests.post(FASTAPI_URL, json=payload)
                response.raise_for_status()  # Raise an exception for bad status codes

                data = response.json()

                # Display the results
                st.divider()
                st.subheader("Answer")
                st.markdown(data['answer'])

                with st.expander("Show Retrieved Context"):
                    st.text(data['sources'])

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend API. Please ensure it is running. Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
