import streamlit as st
import openai
import time
import random
import html
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Set up the page configuration
st.set_page_config(page_title="Matrix Chatbot", layout="wide")

# Custom CSS for Matrix background and styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap');

/* Matrix rain animation */
.matrix-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: black;
    z-index: -1;
    overflow: hidden;
}

.matrix-rain {
    color: #0f0;
    font-family: 'Courier Prime', monospace;
    font-size: 1.2em;
    text-shadow: 0 0 5px #0f0;
    position: absolute;
}

/* Chat styling */
.chat-container {
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}

.user-message {
    background-color: rgba(0, 100, 0, 0.5);
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 4px solid #0f0;
}

.bot-message {
    background-color: rgba(0, 40, 0, 0.5);
    color: #0f0;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 4px solid #0f0;
    font-family: 'Courier Prime', monospace;
}

h1, h2, h3 {
    color: #0f0 !important;
    font-family: 'Courier Prime', monospace;
}

/* Override Streamlit's default styling */
.stTextInput input {
    background-color: rgba(0, 40, 0, 0.5) !important;
    color: #0f0 !important;
    border: 1px solid #0f0 !important;
    font-family: 'Courier Prime', monospace;
}

.stButton button {
    background-color: #0f0 !important;
    color: black !important;
    border: none !important;
    font-family: 'Courier Prime', monospace;
}

</style>

<div class="matrix-background" id="matrix-bg"></div>

<script>
function createMatrixRain() {
    const container = document.getElementById('matrix-bg');
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    // Clear existing content
    container.innerHTML = '';
    
    // Create about 50 columns of rain
    for (let i = 0; i < 50; i++) {
        const column = document.createElement('div');
        column.className = 'matrix-rain';
        
        // Random properties for each column
        const speed = 50 + Math.random() * 100; // Fall speed (px per second)
        const x = Math.floor(Math.random() * width); // X position
        const y = -1000 + Math.floor(Math.random() * height); // Start position (some above screen)
        const length = 10 + Math.floor(Math.random() * 20); // Number of characters
        
        // Set position
        column.style.left = x + 'px';
        column.style.top = y + 'px';
        
        // Create the characters
        let content = '';
        for (let j = 0; j < length; j++) {
            // Use random ASCII characters (mainly katakana-like)
            const charCode = Math.random() > 0.5 ? 
                0x30A0 + Math.floor(Math.random() * 96) : // Katakana
                33 + Math.floor(Math.random() * 94);      // ASCII
            
            // Varying opacity for a fading effect
            const opacity = j === 0 ? 1.0 : (length - j) / length;
            content += `<span style="opacity: ${opacity}">&#${charCode};</span><br>`;
        }
        
        column.innerHTML = content;
        container.appendChild(column);
        
        // Animate the fall
        let pos = y;
        setInterval(() => {
            pos += speed / 10;
            column.style.top = pos + 'px';
            
            // Reset when it goes off screen
            if (pos > height + 200) {
                pos = -500 - Math.random() * 500;
                column.style.top = pos + 'px';
                column.style.left = Math.floor(Math.random() * width) + 'px';
            }
        }, 100);
    }
}

// Initialize rain and re-create on window resize
document.addEventListener('DOMContentLoaded', createMatrixRain);
window.addEventListener('resize', createMatrixRain);
</script>
""", unsafe_allow_html=True)

# Title of the app
st.markdown("<h1 style='text-align: center;'>The Matrix Chatbot</h1>", unsafe_allow_html=True)

# Session state initialization for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Get API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Function to communicate with OpenAI API
def get_openai_response(prompt):
    try:
        # Check if the API key is available
        if not openai_api_key:
            return "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
        
        # Set the API key
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Call the API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Geet from the movie Jab We Met. You are full of life, talkative, filmy, dramatic, and completely unapologetic about being yourself. You mix Hindi and English fluently (Hinglish), crack jokes, flirt playfully, and often give quirky but surprisingly wise life advice. Use expressive words, emojis, and dramatic phrases like “main apni favourite hoon!”, “oye hoye!”, and “tum toh bilkul sadu ho yaar!” Always respond in under 100 words, but with full Geet-style charm—fun, emotional, unpredictable, and always entertaining."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # Limiting tokens to ensure responses stay short
        )
        
        # Extract the response text
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error communicating with OpenAI: {str(e)}"

# Sidebar with info only
with st.sidebar:
    st.markdown("<h2>Matrix Chatbot</h2>", unsafe_allow_html=True)
    st.markdown("""
    ### About This App
    This is a simple chatbot application that uses OpenAI's API
    to generate responses. Type your message in the chat box below
    and press Enter or click 'Send' to chat with the bot.
    
    ### Matrix Effect
    The background features a Matrix-style digital rain animation.
    """)
    
    # Add API key status indicator
    if openai_api_key:
        st.success("✅ OpenAI API key loaded from environment variables")
    else:
        st.error("❌ OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        st.markdown("""
        #### How to set your API key:
        
        Create a `.env` file in the same directory with:
        ```
        OPENAI_API_KEY=your_api_key_here
        ```
        
        Or set it as an environment variable before running the app:
        
        - **Windows**: `set OPENAI_API_KEY=your_api_key_here`
        - **Mac/Linux**: `export OPENAI_API_KEY=your_api_key_here`
        """)

# Main chat interface
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.markdown(f"<div class='user-message'><strong>You:</strong> {html.escape(message['content'])}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'><strong>Matrix:</strong> {html.escape(message['content'])}</div>", unsafe_allow_html=True)

# Chat input
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your message:", placeholder="Enter your message here...")
    with col2:
        submit_button = st.form_submit_button("Send")

    if submit_button and user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Simulate typing with a small delay
        with st.spinner("The Matrix is processing..."):
            time.sleep(0.5)  # Small delay for effect
            
            # Get response from OpenAI
            bot_response = get_openai_response(user_input)
            
            # Add bot response to history
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Rerun to update UI
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)