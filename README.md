# 🤖 SmartAssist AI

SmartAssist AI is an intelligent conversational assistant powered by Google's Gemini 2.5 Flash model and enhanced with real-time web search using Tavily. It combines the reasoning capabilities of large language models with live internet retrieval to deliver accurate, context-aware, and up-to-date responses.

## 🌟 Live Demo

**Try SmartAssist AI:**

https://smartassist-ai-chatbot-2hcsdefpqjxkhnmneywvmd.streamlit.app/

---

## 🚀 Features

### 🧠 AI-Powered Conversations

* Powered by Gemini 2.5 Flash
* Natural and human-like responses
* Context-aware conversations

### 🌐 Live Web Search

* Real-time information retrieval using Tavily
* Fetches current news, trends, and recent events
* Provides more up-to-date responses than static AI knowledge

### 💬 Conversation Memory

* Maintains context from recent interactions
* Supports follow-up questions naturally
* Stores the latest 20 messages in session memory

### 🎨 Modern User Interface

* Built with Streamlit
* Interactive chat interface
* User-friendly sidebar controls
* Dark theme support

### ⚙️ Deployment Ready

* Docker support
* Environment variable configuration
* Cloud deployment using Streamlit Community Cloud

### 🛡️ Error Handling

* Graceful handling of API rate limits
* Search fallback mechanisms
* Improved user experience during failures

---

## 🏗️ Architecture

```text
User
  │
  ▼
SmartAssist UI (Streamlit)
  │
  ├── Tavily Search API
  │       │
  │       ▼
  │   Live Web Results
  │
  ▼
Gemini 2.5 Flash
  │
  ▼
AI Response
```

---

## 🛠️ Tech Stack

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| Python           | Core Programming Language |
| Streamlit        | Web Interface             |
| Gemini 2.5 Flash | Large Language Model      |
| Tavily           | Real-Time Web Search      |
| Docker           | Containerization          |
| Python Dotenv    | Environment Management    |

---

## 📂 Project Structure

```text
SmartAssist-AI-Chatbot/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── README.md
├── .gitignore
│
└── .streamlit/
    └── config.toml
```

---

## ⚡ Local Installation

### Clone Repository

```bash
git clone https://github.com/hemalathanallabariki/SmartAssist-AI-Chatbot.git

cd SmartAssist-AI-Chatbot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Run Application

```bash
streamlit run app.py
```

or

```bash
py -m streamlit run app.py
```

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t smartassist .
```

### Run Container

```bash
docker run -p 8501:8501 smartassist
```

### Access Application

```text
http://localhost:8501
```


---

## 🎯 Future Enhancements

* PDF Chat and Document Q&A
* Retrieval-Augmented Generation (RAG)
* Voice Input and Voice Output
* Multi-Model Support (Gemini/OpenAI)
* Chat Export Functionality
* Source Citations for Responses
* User Authentication

---

## 👩‍💻 Author

**Hema Latha Nallabariki**

Data Science Student
Geethanjali College of Engineering and Technology

---

## ⭐ Key Highlights

* Integrated Gemini 2.5 Flash for conversational AI
* Implemented real-time web search using Tavily
* Added conversational memory for contextual responses
* Containerized using Docker
* Deployed publicly using Streamlit Cloud
* Built a scalable foundation for future RAG-based enhancements
