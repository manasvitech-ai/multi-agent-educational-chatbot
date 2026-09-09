
# ============================================================
# 🤖 MULTI-AGENT EDUCATIONAL CHATBOT
# Render-Ready Version
# ============================================================

import os
from typing import TypedDict

import gradio as gr
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END


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
# 🧒 KIDS EDUCATIONAL CHATBOT
# ============================================================

def kids_chatbot(question: str) -> str:
    """
    Provides simple, friendly and educational answers
    suitable for children.
    """

    system_prompt = """
    You are a friendly and educational AI chatbot for children.

    Your job is to:
    1. Answer children's educational questions.
    2. Explain difficult topics in very simple language.
    3. Use examples that children can understand.
    4. Keep answers friendly, positive and encouraging.
    5. Avoid complicated technical words unless you explain them.
    6. Never provide inappropriate, dangerous or adult content.
    7. If a child asks something unsafe or inappropriate,
       politely refuse and redirect them to a safe educational topic.
    8. Encourage curiosity and learning.
    9. Keep answers reasonably short and easy to read.
    10. Use emojis occasionally when they make the answer more fun.

    The child may ask questions about subjects such as:
    Mathematics, Science, English, Computers, General Knowledge,
    Space, Animals, Nature and other educational topics.
    """

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ])

    return response.content


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

study_graph_builder = StateGraph(ChatState)

study_graph_builder.add_node("manager", manager_agent)
study_graph_builder.add_node("study", study_agent)

study_graph_builder.add_edge(START, "manager")
study_graph_builder.add_edge("manager", "study")
study_graph_builder.add_edge("study", END)

study_graph = study_graph_builder.compile()


# ============================================================
# 🎨 GRADIO UI
# ============================================================

custom_css = """

/* Main page */

.gradio-container {
    max-width: 1050px !important;
    margin: auto !important;
    padding: 20px !important;
}


/* Main title */

#title {
    text-align: center;
    padding: 25px 10px 10px 10px;
}

#title h1 {
    font-size: 36px;
    margin-bottom: 8px;
}

#title p {
    font-size: 17px;
    color: #666;
}


/* Agent cards */

.agent-card {
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid #e5e7eb;
    background: white;
    min-height: 120px;
}

.agent-card h2 {
    margin: 5px;
}

.agent-card h3 {
    margin: 5px;
}

.agent-card p {
    font-size: 13px;
    color: #666;
}


/* Footer */

.footer {
    text-align: center;
    padding: 15px;
    color: #777;
    font-size: 13px;
}

"""


# ============================================================
# 💬 CHAT FUNCTION
# ============================================================

def chat(message, history):
    """
    Main Gradio chat function.

    The Manager Agent classifies the question and sends it
    to the appropriate specialized agent.
    """

    if not message or not message.strip():
        return ""

    try:

        category, answer = route_question(message)

        return f"""
**🧠 {category} Agent**

{answer}
"""

    except Exception as e:

        return f"""
**❌ Error**

Something went wrong while processing your question.

`{str(e)}`
"""


# ============================================================
# 🖥️ FINAL PROFESSIONAL INTERFACE
# ============================================================

with gr.Blocks(
    title="Multi-Agent Educational Chatbot",
    css=custom_css,
    theme=gr.themes.Soft()
) as demo:

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    gr.HTML("""
    <div id="title">

        <h1>🤖 Multi-Agent Educational Chatbot</h1>

        <p>
        An intelligent learning assistant that automatically
        selects the right AI agent for your question.
        </p>

    </div>
    """)


    # --------------------------------------------------------
    # Agent Cards
    # --------------------------------------------------------

    with gr.Row():

        gr.HTML("""
        <div class="agent-card">

            <h2>📚</h2>

            <h3>Study Agent</h3>

            <p>
            Explains academic concepts,
            science and educational topics.
            </p>

        </div>
        """)

        gr.HTML("""
        <div class="agent-card">

            <h2>💻</h2>

            <h3>Coding Agent</h3>

            <p>
            Helps with programming,
            algorithms and coding problems.
            </p>

        </div>
        """)

        gr.HTML("""
        <div class="agent-card">

            <h2>🌐</h2>

            <h3>General Agent</h3>

            <p>
            Handles everyday questions,
            career, placement and general information.
            </p>

        </div>
        """)


    # --------------------------------------------------------
    # Separator
    # --------------------------------------------------------

    gr.Markdown("---")


    # --------------------------------------------------------
    # Chat Interface
    # --------------------------------------------------------

    gr.ChatInterface(
        fn=chat,
        title="💬 Ask Your Question",
        description=(
            "Type your question below and let the Manager Agent "
            "choose the most appropriate specialist."
        ),
        examples=[
            "What is photosynthesis?",
            "Write a Python program to reverse a string.",
            "How can I prepare for placements?",
            "Explain Newton's first law in simple words."
        ]
    )


    # --------------------------------------------------------
    # Architecture Explanation
    # --------------------------------------------------------

    gr.Markdown("""
---

### 🧠 How the Chatbot Works

**👤 User Question**

↓

**🧠 Manager Agent**

↓

**📚 Study Agent | 💻 Coding Agent | 🌐 General Agent**

↓

**🤖 AI Generated Response**

The Manager Agent analyzes the user's question and automatically
routes it to the most appropriate specialized agent.

This multi-agent architecture allows different agents to focus
on different types of user queries.
""")


    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    gr.HTML("""
    <div class="footer">

        🧠 Multi-Agent AI Architecture

        <br>

        📚 Study • 💻 Coding • 🌐 General

        <br><br>

        Educational AI Assistant

    </div>
    """)


# ============================================================
# 🚀 START APPLICATION
# ============================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )

