
# ============================================================
# 🤖 MULTI-AGENT EDUCATIONAL CHATBOT
# Render-Ready Version
# ============================================================

import os
from typing import TypedDict

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage



# ============================================================
# 🔐 API CONFIGURATION
# ============================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. "
        "Please add it as an Environment Variable in Render."
    )


# ============================================================
# 🤖 LANGUAGE MODELS
# ============================================================

# Main LLM used by Manager, Study and Kids agents
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=GROQ_API_KEY
)


# Coding Agent uses a lower temperature for more consistent code
coding_llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3,
    api_key=GROQ_API_KEY
)


# General Agent
general_llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=GROQ_API_KEY
)





# ============================================================
# 🧠 CHAT STATE
# ============================================================

class ChatState(TypedDict):
    user_message: str
    response: str


# ============================================================
# 🧠 MANAGER AGENT
# ============================================================

def manager_agent(state: ChatState) -> ChatState:
    """
    Classifies the user's question into one of three categories:
    STUDY, CODING or GENERAL.
    """

    user_message = state["user_message"]

    prompt = f"""
You are the Manager Agent of a general-purpose AI chatbot.

Classify the user's question into exactly ONE category:

- STUDY: questions about academic subjects, explanations,
  education or learning

- CODING: programming, Python, Java, algorithms, debugging
  or technical coding

- GENERAL: everything else, including career, placement,
  daily life and general questions

User question:
{user_message}

Reply with ONLY one word:

STUDY
CODING
or
GENERAL
"""

    response = llm.invoke(prompt)

    category = response.content.strip().upper()

    # Safety fallback if the model returns something unexpected
    if category not in ["STUDY", "CODING", "GENERAL"]:
        category = "GENERAL"

    return {
        **state,
        "response": category
    }


# ============================================================
# 📚 STUDY AGENT
# ============================================================

def study_agent(state: ChatState) -> ChatState:
    """
    Handles educational and academic questions.
    """

    user_message = state["user_message"]

    prompt = f"""
You are a helpful Study Agent in a general-purpose AI chatbot.

Answer the user's educational question clearly and accurately.

Rules:
- Explain concepts in simple language.
- Use examples when helpful.
- Use headings or bullet points when appropriate.
- If the question is difficult, break it into smaller parts.
- Do not assume the user's age or class.
- Do not answer questions unrelated to education.

User question:
{user_message}
"""

    response = llm.invoke(prompt)

    return {
        **state,
        "response": response.content
    }


# ============================================================
# 💻 CODING AGENT
# ============================================================

def coding_agent(question: str) -> str:
    """
    Handles programming, debugging and technical questions.
    """

    prompt = f"""
You are a helpful Coding Agent in an educational chatbot.

Your job is to answer programming and coding-related questions.

Follow these rules:

1. Explain the concept in simple language.
2. Provide correct and working code when the user asks
   for a program.
3. Explain the code step by step.
4. If the user asks for debugging, identify the error
   and provide the corrected code.
5. Use examples wherever useful.
6. Do not answer unrelated questions.
7. If the programming language is not specified,
   use Python by default when code is required.

User Question:
{question}
"""

    response = coding_llm.invoke(prompt)

    return response.content


# ============================================================
# 🌐 GENERAL AGENT
# ============================================================

def general_agent(question: str) -> str:
    """
    Handles general, career, placement and everyday questions.
    """

    prompt = f"""
You are the General Agent of an educational multi-agent chatbot.

Your job is to answer general questions that do not specifically
belong to Study or Coding.

Rules:

1. Give clear and useful answers.
2. Use simple and understandable language.
3. Be friendly and helpful.
4. Use examples when useful.
5. Do not provide programming code unless it is specifically requested.
6. If the question is about studying a subject, it should normally
   be handled by the Study Agent instead.
7. If the question is specifically about programming or coding,
   it should normally be handled by the Coding Agent.

User Question:
{question}
"""

    response = general_llm.invoke(prompt)

    return response.content


# ============================================================
# 🔀 MULTI-AGENT ROUTER
# ============================================================

def route_question(question: str):
    """
    Connects the Manager Agent with the three specialized agents.

    Flow:

    User Question
          ↓
    Manager Agent
          ↓
    ┌───────────────┬───────────────┬───────────────┐
    │ Study Agent   │ Coding Agent  │ General Agent │
    └───────────────┴───────────────┴───────────────┘
          ↓
      Final Answer
    """

    state: ChatState = {
        "user_message": question,
        "response": ""
    }

    # Step 1: Manager determines the category
    manager_result = manager_agent(state)

    category = manager_result["response"]

    # Step 2: Route to the appropriate specialized agent
    if category == "STUDY":

        result = study_agent(state)
        answer = result["response"]

    elif category == "CODING":

        answer = coding_agent(question)

    else:

        answer = general_agent(question)

    return category, answer


# ============================================================
# 🧠 LANGGRAPH IMPLEMENTATION
# ============================================================

def chat_agent(state: ChatState) -> ChatState:
    """
    Basic LangGraph chat agent retained from the original project.
    """

    user_message = state["user_message"]

    response = llm.invoke(user_message)

    return {
        "user_message": user_message,
        "response": response.content
    }


# Basic LangGraph chatbot
graph_builder = StateGraph(ChatState)

graph_builder.add_node("chat_agent", chat_agent)

graph_builder.add_edge(START, "chat_agent")
graph_builder.add_edge("chat_agent", END)

chatbot_graph = graph_builder.compile()


# ============================================================
# 📚 STUDY LANGGRAPH
# ============================================================



# ============================================================
# 🌐 WEB API + MODERN HTML/CSS/JS FRONTEND
# ============================================================

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.get("/")
def home():
    """Serve the modern frontend."""
    return render_template("index.html")


@app.get("/health")
def health():
    """Simple deployment health check."""
    return jsonify({"status": "ok"})


@app.post("/chat")
def chat_api():
    """
    API endpoint used by the HTML/CSS/JavaScript frontend.

    The actual answer always comes from the existing multi-agent
    route_question() function.
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "success": False,
            "error": "Please enter a question."
        }), 400

    try:
        category, answer = route_question(message.strip())

        return jsonify({
            "success": True,
            "agent": category,
            "answer": answer
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Something went wrong while processing your question.",
            "details": str(e)
        }), 500


# ============================================================
# 🚀 START APPLICATION
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
