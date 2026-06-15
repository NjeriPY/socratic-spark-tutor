import streamlit as st
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from groq import Groq

# --- 1. SETUP & KEY LOADING ---
load_dotenv()
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# --- 2. THE "LOCK" ON STATE ---
# We check if 'messages' exists. If it does, Streamlit skips this and keeps your history.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I’m your AI learning assistant. I help you learn step by step, check your understanding, and guide you until you're confident. \n\nWhat topic would you like to learn today?"}
    ]

if "research_metadata" not in st.session_state:
    st.session_state.research_metadata = ""

# --- 3. UI BRANDING ---
st.set_page_config(page_title="The Socratic Spark", page_icon="🎓")
st.title("🎓 The Socratic Spark")

# --- 4. CONTINUOUS HISTORY DISPLAY ---
# This loop runs EVERY time the app reruns, ensuring you can always scroll up.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT INPUT & LOGIC ---
if prompt := st.chat_input("Your answer or topic..."):
    
    # Add User Message to State
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display it immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Response Logic
    with st.chat_message("assistant"):
        # SILENT RESEARCH (Runs only once at the start)
        if len(st.session_state.messages) == 2:
            with st.spinner("Scouting concepts..."):
                try:
                    tavily = TavilyClient(api_key=TAVILY_API_KEY)
                    search = tavily.search(query=prompt, search_depth="advanced")
                    st.session_state.research_metadata = "\n".join([r['content'] for r in search['results']])
                except:
                    pass

        # GROQ CALL
        client = Groq(api_key=GROQ_API_KEY)
        system_prompt = f"You are a Socratic tutor. Research context: {st.session_state.research_metadata}"
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # CRITICAL: This ensures the UI refreshes to show the full scrolled history properly
            st.rerun()

        except Exception as e:
            st.error("The tutor is taking a quick break (API Timeout). Please try sending your last message again!")