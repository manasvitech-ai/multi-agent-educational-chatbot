const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const messages = document.getElementById("messages");
const welcome = document.getElementById("welcome");
const typingWrap = document.getElementById("typingWrap");
const agentProcessing = document.getElementById("agentProcessing");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const newChatBtn = document.getElementById("newChatBtn");
const recentChats = document.getElementById("recentChats");
const toast = document.getElementById("toast");
const mobileMenu = document.getElementById("mobileMenu");
const sidebar = document.getElementById("sidebar");
const mobileOverlay = document.getElementById("mobileOverlay");

let chatHistory = JSON.parse(localStorage.getItem("edumind_history") || "[]");

function escapeHtml(value) {
    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function formatAnswer(text) {
    let safe = escapeHtml(String(text));

    // Basic Markdown-like formatting for readable AI answers.
    safe = safe.replace(/```([\s\S]*?)```/g, (_, code) =>
        `<pre><code>${code.trim()}</code></pre>`
    );
    safe = safe.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    safe = safe.replace(/\n/g, "<br>");

    return safe;
}

function timeNow() {
    return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function scrollBottom() {
    const area = document.getElementById("chatArea");
    area.scrollTo({ top: area.scrollHeight, behavior: "smooth" });
}

function addMessage(role, text, agent = null, time = timeNow()) {
    welcome.classList.add("hidden");

    const row = document.createElement("div");
    row.className = `message-row ${role}`;

    const avatar = document.createElement("div");
    avatar.className = `message-avatar ${role === "ai" ? "ai-avatar" : "user-avatar"}`;
    avatar.textContent = role === "ai" ? "✦" : "You";

    const bubble = document.createElement("div");
    bubble.className = `bubble ${role === "ai" ? "ai-bubble" : "user-bubble"}`;

    if (role === "ai" && agent) {
        const icons = { STUDY: "📚", CODING: "💻", GENERAL: "🌐" };
        bubble.innerHTML = `
            <div class="agent-tag">${icons[agent] || "✦"} ${agent} AGENT</div>
            <div>${formatAnswer(text)}</div>
            <div class="message-time">${time}</div>
        `;
    } else {
        bubble.innerHTML = `<div>${formatAnswer(text)}</div><div class="message-time">${time}</div>`;
    }

    row.appendChild(avatar);
    row.appendChild(bubble);
    messages.appendChild(row);
    scrollBottom();
}

function setLoading(loading) {
    typingWrap.classList.toggle("hidden", !loading);
    sendBtn.disabled = loading;
    messageInput.disabled = loading;
    if (loading) scrollBottom();
}

function showToast(message) {
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2400);
}

function saveHistory() {
    localStorage.setItem("edumind_history", JSON.stringify(chatHistory.slice(-20)));
}

function renderRecent() {
    if (!chatHistory.length) {
        recentChats.innerHTML = `<div class="empty-recent">Your conversations will appear here.</div>`;
        return;
    }

    recentChats.innerHTML = "";
    [...chatHistory].reverse().slice(0, 8).forEach((item, index) => {
        const btn = document.createElement("button");
        btn.className = "recent-item";
        btn.textContent = item.message;
        btn.title = item.message;
        btn.onclick = () => {
            clearConversation(false);
            addMessage("user", item.message);
            addMessage("ai", item.answer, item.agent);
            sidebar.classList.remove("open");
            mobileOverlay.classList.remove("show");
        };
        recentChats.appendChild(btn);
    });
}

async function sendMessage(message) {
    const clean = message.trim();
    if (!clean) return;

    addMessage("user", clean);
    messageInput.value = "";
    autoResize();
    setLoading(true);

    const stages = [
        "Manager Agent is routing your question",
        "Selecting the most suitable specialist",
        "Generating your answer"
    ];

    let stage = 0;
    agentProcessing.textContent = stages[stage];
    const stageTimer = setInterval(() => {
        stage = (stage + 1) % stages.length;
        agentProcessing.textContent = stages[stage];
    }, 900);

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: clean })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || "Unable to process the question.");
        }

        addMessage("ai", data.answer, data.agent);

        chatHistory.push({
            message: clean,
            answer: data.answer,
            agent: data.agent,
            time: timeNow()
        });
        saveHistory();
        renderRecent();

    } catch (error) {
        addMessage(
            "ai",
            `I couldn't process that request right now.\n\nError: ${error.message}`,
            "GENERAL"
        );
        showToast("Something went wrong. Please try again.");
    } finally {
        clearInterval(stageTimer);
        setLoading(false);
        messageInput.focus();
    }
}

function clearConversation(showMessage = true) {
    messages.innerHTML = "";
    welcome.classList.remove("hidden");
    if (showMessage) showToast("Chat cleared");
}

function autoResize() {
    messageInput.style.height = "auto";
    messageInput.style.height = Math.min(messageInput.scrollHeight, 140) + "px";
}

chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    sendMessage(messageInput.value);
});

messageInput.addEventListener("input", autoResize);

messageInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        chatForm.requestSubmit();
    }
});

document.querySelectorAll(".agent-card").forEach(card => {
    card.addEventListener("click", () => {
        messageInput.value = card.dataset.prompt;
        autoResize();
        messageInput.focus();
    });
});

clearBtn.addEventListener("click", () => clearConversation());
newChatBtn.addEventListener("click", () => {
    clearConversation();
    sidebar.classList.remove("open");
    mobileOverlay.classList.remove("show");
    messageInput.focus();
});

mobileMenu.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    mobileOverlay.classList.toggle("show");
});

mobileOverlay.addEventListener("click", () => {
    sidebar.classList.remove("open");
    mobileOverlay.classList.remove("show");
});

renderRecent();
