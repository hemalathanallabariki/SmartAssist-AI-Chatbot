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
st.caption(
    "Powered by Gemini 2.5 Flash + Tavily Live Search"
)

# -------------------------
# SIDEBAR
# -------------------------

with st.sidebar:

    st.title("🤖 SmartAssist")
    
    search_mode = st.toggle(
        "🌐 Live Web Search",
        value=True
    )
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Model",
            "Gemini"
        )

    with col2:
        st.metric(
            "Search",
            "ON" if search_mode else "OFF"
        )

    with col3:
        st.metric(
            "Messages",
            len(st.session_state.get("messages", []))
        )

    st.markdown(
        "AI Assistant powered by Gemini and Tavily"
    )

    st.divider()

    

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.info(
        """
        **Model:** Gemini 2.5 Flash
        
        **Search:** Tavily AI
        
        **Memory:** Last 20 messages
        """
    )

# -------------------------
# CHAT HISTORY
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
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

    with st.chat_message(
        "user",
        avatar="👤"
    ):
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

                for item in results["results"]:
                    web_context += (
                        f"Title: {item['title']}\n"
                        f"URL: {item['url']}\n"
                        f"Content: {item['content']}\n\n"
                    )
            except Exception as e:
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

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            with st.spinner("Thinking..."):
                try:
                    response = model.generate_content(
                        final_prompt
                    )

                    bot_reply = response.text

                except Exception as e:

                    if "429" in str(e):
                        bot_reply = (
                            "⚠️ Gemini API rate limit reached. "
                            "Please wait a few seconds and try again."
                        )
                    else:
                        bot_reply = (
                            "⚠️ Something went wrong while generating the response."
                        )

                st.markdown(bot_reply)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_reply
            }
        )

    except Exception as e:
        st.error(str(e))