# 🤖 Multi-Agent Educational Chatbot

An intelligent **multi-agent educational chatbot** that automatically understands a user's question and routes it to the most suitable AI agent.

The system uses **LangGraph**, **LangChain**, and **Groq LLMs** to create specialized agents for study, coding, and general queries, with an interactive **Gradio** chat interface.

---

## ✨ Features

* 🧠 **Intelligent Query Routing**
* 📚 **Study Agent** for academic and educational questions
* 💻 **Coding Agent** for programming, debugging, and DSA
* 💬 **General Agent** for general-purpose queries
* 🤖 **Manager Agent** for deciding which agent should handle a question
* 🔗 **LangGraph-based Multi-Agent Architecture**
* ⚡ **Groq-powered LLM responses**
* 🎨 **Interactive Gradio Web Interface**
* 🖥️ Custom chatbot UI with agent information and example questions
* 🧩 Modular and extensible architecture

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Gradio UI      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Manager Agent    │
                    │   Query Classifier  │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │ Study Agent │   │Coding Agent │   │General Agent│
      └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │    AI Response      │
                    └─────────────────────┘
```


---

## 🔄 How It Works

1. The user enters a question through the **Gradio interface**.
2. The **Manager Agent** analyzes the question.
3. The question is classified into one of three categories:

   * `STUDY`
   * `CODING`
   * `GENERAL`
4. The question is routed to the corresponding specialized agent.
5. The selected agent generates a response using the Groq LLM.
6. The response is displayed to the user through the Gradio interface.

---

## 🤖 Agents

### 🧠 Manager Agent

The Manager Agent acts as the **router** of the system.

It analyzes the user's query and determines which specialized agent should handle it.

```text
User Query
    ↓
Manager Agent
    ↓
┌──────────────┬──────────────┬──────────────┐
│    STUDY     │    CODING    │    GENERAL   │
└──────────────┴──────────────┴──────────────┘
```

---

### 📚 Study Agent

The Study Agent is designed for educational and academic questions.

It can handle:

* Computer Science concepts
* Mathematics and Science
* Academic explanations
* Exam preparation
* Study-related questions

**Example:**

`What is the difference between supervised and unsupervised learning?`

→ Routed to **Study Agent**

---

### 💻 Coding Agent

The Coding Agent handles programming-related questions.

It can help with:

* Programming concepts
* Python, C++, and other languages
* Data Structures and Algorithms
* Debugging
* Code explanations
* Programming problems

If the user does not specify a programming language, the agent can default to **Python**.

**Example:**

`Write a Python program to implement binary search.`

→ Routed to **Coding Agent**

---

### 💬 General Agent

The General Agent handles queries that do not specifically belong to study or coding.

Examples include:

* Career-related questions
* Placement preparation
* General advice
* Everyday questions
* Non-technical queries

**Example:**

`How should I prepare for my first technical interview?`

→ Routed to **General Agent**

---

## 🛠️ Tech Stack

| Technology            | Purpose                          |
| --------------------- | -------------------------------- |
| Python                | Core programming language        |
| LangChain             | LLM application framework        |
| LangGraph             | Multi-agent workflow and routing |
| Groq                  | LLM inference                    |
| Llama / GPT-OSS       | Language models                  |
| Gradio                | Web-based chatbot interface      |
| Wikipedia             | Knowledge retrieval support      |
| Environment Variables | API key management               |

---

## 📁 Project Structure

```text
multiagent-educational-chatbot/
│
├── .devcontainer/
│
├── app.py
│
├── requirements.txt
│
└── README.md
```

---

## 🔑 API Keys

This project requires a **Groq API key** to access the language models.

Set your API key as an environment variable:

```text
GROQ_API_KEY=your_groq_api_key
```

If Tavily-based web search is enabled in the future, a Tavily API key can also be added:

```text
TAVILY_API_KEY=your_tavily_api_key
```

**Never commit your API keys directly to GitHub.**

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/manasvitech-ai/multi-agent-educational-chatbot.git
```

### 2. Navigate to the project directory

```bash
cd multi-agent-educational-chatbot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

Recommended dependencies for the current Gradio-based application:

```text
gradio
langgraph
langchain-groq
langchain-community
langchain-tavily
langchain-core
wikipedia
groq
```

---

## ▶️ Run the Application

After setting the required API key, run:

```bash
python app.py
```

The Gradio interface will launch and provide an interactive chatbot UI.

---

## 💡 Example Queries

### 📚 Study

* Explain operating system deadlock in simple terms.
* What is supervised learning?
* Explain the difference between TCP and UDP.

### 💻 Coding

* Write a C++ program for binary search.
* Explain recursion with an example.
* Debug this Python code.

### 💬 General

* How should I prepare for placements?
* What skills are important for a software engineering internship?

---

## 🔀 Example Routing

### Study Query

```text
"Explain how photosynthesis works."
          ↓
   Manager Agent
          ↓
        STUDY
          ↓
     Study Agent
          ↓
       Response
```

### Coding Query

```text
"Write a C++ program for binary search."
          ↓
   Manager Agent
          ↓
       CODING
          ↓
    Coding Agent
          ↓
       Response
```

### General Query

```text
"How can I improve my interview skills?"
          ↓
   Manager Agent
          ↓
       GENERAL
          ↓
    General Agent
          ↓
       Response
```

---

## 🎨 User Interface

The project includes an interactive **Gradio-based frontend**.

The interface provides:

* Chat window
* User input
* Example questions
* Agent information
* Custom styling
* Multi-agent architecture explanation

The **frontend and AI/backend logic are currently implemented together inside `app.py` using Gradio**.

---

## 🧩 Why Multi-Agent Architecture?

Instead of using one general-purpose chatbot for every query, this project divides responsibilities between specialized agents.

### Advantages

* **Specialization** — each agent focuses on a specific type of task.
* **Better Routing** — questions are automatically sent to the appropriate agent.
* **Modularity** — agents can be modified independently.
* **Scalability** — new agents can be added later.
* **Maintainability** — responsibilities are separated logically.

---

## 🚀 Future Improvements

* 🌐 Real-time web search using Tavily
* 📄 PDF and document-based question answering
* 🔎 Retrieval-Augmented Generation (RAG)
* 🧮 Dedicated Mathematics Agent
* 📝 Exam Preparation Agent
* 🧠 Conversation memory
* 👤 Personalized student profiles
* 📊 Learning progress tracking
* 🌍 Multilingual support
* 🎙️ Voice-based interaction
* 🔐 User authentication
* 🗄️ Vector database integration
* ☁️ Cloud deployment
* 📱 Improved responsive UI
* 🔌 Separate frontend and backend architecture

---

## 📌 Current Project Status

This project was developed iteratively while experimenting with **LangChain, LangGraph, Groq LLMs, multi-agent routing, and Gradio**.

The current `app.py` contains experimental and test sections from the development process.

For a production-ready version, the architecture can be further refactored into:

```text
Frontend
    ↓
Backend API
    ↓
Manager Agent
    ↓
Specialized Agents
    ↓
LLM / Tools
```

---

## 📚 Learning Objectives

This project demonstrates practical implementation of:

* Large Language Models (LLMs)
* Generative AI
* LangChain
* LangGraph
* Multi-Agent Systems
* Agent Routing
* Prompt Engineering
* API Integration
* Gradio Interfaces
* Python-based AI Applications

---

## 🌟 Project Highlights

| Feature                  | Status                |
| ------------------------ | --------------------- |
| Multi-Agent Architecture | ✅                     |
| Manager Agent            | ✅                     |
| Study Agent              | ✅                     |
| Coding Agent             | ✅                     |
| General Agent            | ✅                     |
| LangGraph Workflow       | ✅                     |
| Groq LLM Integration     | ✅                     |
| Gradio Frontend          | ✅                     |
| Custom Chat UI           | ✅                     |
| Tavily Search            | 🔄 Future Enhancement |
| RAG                      | 🔄 Future Enhancement |
| Persistent Memory        | 🔄 Future Enhancement |

---

## 🔮 Future Vision

The goal is to evolve this project into a complete **AI-powered educational assistant** capable of providing personalized learning support.

The future system can combine:

```text
                 AI Educational Assistant
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   Study Agent       Coding Agent      Career Agent
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                    Knowledge / RAG
                          │
                          ▼
                    Personalized
                     Responses
```

This can eventually become a unified platform for **learning, coding, exam preparation, research, and career guidance**.

---

## 👩‍💻 Author

**Riya Chaudhary**

B.Tech — Computer Science Engineering

---

## ⭐ Support

If you found this project interesting, consider giving the repository a ⭐ on GitHub!

---

**Built with Python, LangGraph, LangChain, Groq, and Gradio.**
