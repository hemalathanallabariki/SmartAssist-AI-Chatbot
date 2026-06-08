from dotenv import load_dotenv
import os

import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient

# -------------------------
# API KEYS
# -------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# -------------------------
# CONFIGURE APIs
# -------------------------

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

tavily = TavilyClient(api_key=TAVILY_API_KEY)

# -------------------------
# SYSTEM PROMPT
# -------------------------

SYSTEM_PROMPT = """
You are SmartAssist.

You are friendly, knowledgeable and conversational.

Use the web search results when provided.
If web results are available, prioritize them over old knowledge.

Give clear, practical answers.
"""

# -------------------------
# PAGE
# -------------------------

st.set_page_config(
    page_title="SmartAssist",
    page_icon="🤖"
)

st.title("🤖 SmartAssist AI")

# -------------------------
# SIDEBAR
# -------------------------

search_mode = st.sidebar.checkbox(
    "Enable Live Web Search",
    value=True
)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -------------------------
# CHAT HISTORY
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# USER INPUT
# -------------------------

prompt = st.chat_input("Ask me anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:

        # Keep recent conversation
        recent_messages = st.session_state.messages[-20:]

        conversation_history = ""

        for msg in recent_messages:
            conversation_history += (
                f"{msg['role']}: {msg['content']}\n"
            )

        # Search only for current/recent topics
        web_context = ""

        if search_mode:
            try:
                results = tavily.search(
                    query=prompt,
                    search_depth="advanced",
                    max_results=5
                )
                st.sidebar.write("Search Results Found:", len(results["results"]))

                for item in results["results"]:
                    web_context += (
                        f"Title: {item['title']}\n"
                        f"URL: {item['url']}\n"
                        f"Content: {item['content']}\n\n"
                    )
            except Exception:
                web_context=""  
                st.warning(f"Web search unavailable: {e}")    
        final_prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{conversation_history}

Web Search Results:
{web_context}

Current User Question:
{prompt}

Instructions:
- Use conversation history for context.
- Use web results only when available.
- If the user asks about something mentioned earlier in the conversation,
  answer from the conversation history.
- Answer naturally like a human mentor.
"""

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = model.generate_content(
                    final_prompt
                )

                bot_reply = response.text

                st.markdown(bot_reply)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_reply
            }
        )

    except Exception as e:
        st.error(str(e))