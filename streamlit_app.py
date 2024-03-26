import streamlit as st
import httpx
import asyncio

st.title('🎈 Simple Chat App')

# Retrieve webhook URL from Streamlit secrets
WEBHOOK_URL = st.secrets["webhook_url"]

# Input for messages
message = st.text_input("Enter your message:")

# Container to display responses, using text_area for better wrapping
response_container = st.empty()

# Asynchronous function to call the webhook with a custom timeout
async def call_webhook(message):
    # Set a custom timeout (e.g., 120 seconds)
    timeout = httpx.Timeout(120.0, connect=180.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(WEBHOOK_URL, json={"message": message})
        return response.json()

# Function to handle sending messages
async def send_message():
    # Call the webhook and wait for the response
    answer = await call_webhook(message)
    
    # Update the UI with the response using text_area for better wrapping
    response_container.text_area("Response:", answer.get("response", "No response"), height=200)

# Button to send the message
if st.button("Send"):
    # Display a placeholder while waiting for the response
    with st.spinner("Waiting for response..."):
        # Use Streamlit's run_in_thread method to run the async function without blocking
        st.experimental_singleton(send_message)
