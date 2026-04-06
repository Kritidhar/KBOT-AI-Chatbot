import streamlit as st 
#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# then write .\\activate
#cd ..
# start web server by typing "streamlit run app.py"
# pip install -q -U google-generativeai streamlit
# then url will appear


import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="KBot", layout="centered")

# 2. FIXED TITLE CSS
# This CSS makes the title stay at the top (sticky) and adds a background 
# so the chat text doesn't overlap visibly when it scrolls under.
st.markdown(
    """
    <style>
    .fixed-header {
        position: sticky;
        top: 0;
        left: 0;
        width: 100%;
        /* These variables change automatically based on Light/Dark mode */
        background-color: var(--background-color); 
        color: var(--text-color);
        
        z-index: 999;
        text-align: center;
        padding: 20px 0;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    }
    
    .main .block-container {
        padding-top: 100px;
    }
    
    /* This ensures the title text inside matches the mode */
    .fixed-header h1 {
        color: var(--text-color);
        margin: 0;
    }
    </style>
    
    <div class="fixed-header">
        <h1>WELCOME TO KBOT!!</h1>
    </div>
    """,
    unsafe_allow_html=True
)


       

#2. Hide avatars for both user and assistant
st.markdown("""
    <style>
        [data-testid="stChatMessageAvatarUser"],
        [data-testid="stChatMessageAvatarAssistant"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)
            
            
# 3. Your API Key
# GOOGLE_API_KEY = "AIzaSyDgqldVrMwbiNrvTAkRvwcm2GbzmG3MEjA"
# genai.configure(api_key=GOOGLE_API_KEY)

# 3. Your API Key
# We are now using Streamlit Secrets instead of a hardcoded key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Initialize the Model
# Using 'gemini-2.5-flash' which is the current stable standard.
try:
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    # If 2.5 is not yet in your region, this is the universal 'latest' alias
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    

#4. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Input Logic
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            # This will show you exactly why it fails if it happens again
            st.error(f"Error: {e}")

#6. Sidebar
with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()