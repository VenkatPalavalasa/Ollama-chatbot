import streamlit as st
import ollama

# Configure the web page layout
st.set_page_config(page_title="Local Ollama Chat", page_icon="🤖", layout="centered")
st.title("🤖 My Local Ollama Chatbot")

# --- STEP 1: Fetch Available Local Models ---
try:
    model_list_data = ollama.list()
    # Extract model names from the local Ollama registry
    all_models = [m.model for m in model_list_data.models]

    # FILTER: Exclude embedding models that break the chat functionality
    available_models = [m for m in all_models if "embed" not in m.lower()]

    # Fallback to avoid an empty list if only embedding models exist
    if not available_models:
        available_models = ["llama3.2"]
except Exception:
    # Fallback if the Ollama service isn't running or accessible
    available_models = ["llama3.2"]

# --- STEP 2: UI Sidebar Setup ---
st.sidebar.title("Settings")
selected_model = st.sidebar.selectbox(
    "Choose a Model:",
    options=available_models,
    index=available_models.index("llama3.2") if "llama3.2" in available_models else 0
)

# Clear chat button
if st.sidebar.button("Clear Conversation History"):
    st.session_state.messages = []
    st.rerun()

# --- STEP 3: Initialize Conversation History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- STEP 4: Render Existing Chat Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- STEP 5: Handle New User Input ---
if user_input := st.chat_input("Type your question here..."):
    # 1. Display the user's message in the UI instantly
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Append the user message to session memory
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 3. Stream the AI response block
    with st.chat_message("assistant"):
        # Setup streaming connection to local Ollama instance
        response_stream = ollama.chat(
            model=selected_model,
            messages=st.session_state.messages,
            stream=True  # Enables word-by-word streaming animation
        )

        # Use streamlit's built-in chat streamer wrapper
        response_text = st.write_stream(chunk.message.content for chunk in response_stream)

    # 4. Save the finished assistant response to session memory
    st.session_state.messages.append({"role": "assistant", "content": response_text})
