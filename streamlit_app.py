import streamlit as st
import httpx
import asyncio

st.title('🎈 Simple Chat App')

# Retrieve webhook URL from Streamlit secrets
WEBHOOK_URL = st.secrets["webhook_url"]

# Input for messages
message = st.text_input("Enter your message:")

# Container to display responses
response_container = st.empty()

# Asynchronous function to call the webhook with a custom timeout
async def call_webhook(message):
    # Set a custom timeout (e.g., 30 seconds)
    # The timeout can be a float or int and represents the number of seconds to wait before timing out
    timeout = httpx.Timeout(30.0, connect=60.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(WEBHOOK_URL, json={"message": message})
        return response.json()

# Function to handle sending messages
def send_message():
    response_container.text("Sending message...")

    # Workaround for Streamlit's lack of direct asyncio support
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Call the webhook and wait for the response
    response = loop.run_until_complete(call_webhook(message))

    # Update the UI with the response
    response_container.text(response.get("response", "No response"))

if st.button("Send"):
    send_message()
