import streamlit as st
import httpx
import asyncio

st.title('📡 Mă poate ajuta workshopul de AI cu...')

# Retrieve webhook URL from Streamlit secrets
WEBHOOK_URL = st.secrets["webhook_url"]

# Input for messages
message = st.text_input("Scrie aici cu ce ți-ai dori ajutor în munca academică")

# Container to display responses
response_container = st.empty()

# Asynchronous function to call the webhook with a custom timeout
async def call_webhook(message):
    # Set a custom timeout (e.g., 30 seconds)
    # The timeout can be a float or int and represents the number of seconds to wait before timing out
    timeout = httpx.Timeout(60.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(WEBHOOK_URL, json={"message": message})
        return response.json()

# Function to handle sending messages
def send_message():
    response_container.markdown("Sending message...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Call the webhook and wait for the response
        response = loop.run_until_complete(call_webhook(message))

        # Ensure the 'response' variable is directly used after its definition
        # Update the UI with the response using Markdown for better text wrapping
        response_container.markdown(response.get("response", "No response"))
    except Exception as e:
        # Handle exceptions and display an error message
        response_container.markdown(f"An error occurred: {str(e)}")

if st.button("Send"):
    send_message()
