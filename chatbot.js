/**
 * Freddy's Portfolio Chatbot
 * 80's Terminal-Aesthetic Chat Bubble
 */

class FreddyChatbot {
  constructor() {
    this.isOpen = false;
    this.messages = [];
    this.currentPage = this.detectPage();
    this.apiUrl = "http://localhost:8001/api/chat";
    this.init();
  }

  init() {
    this.createChatBubble();
    this.attachEventListeners();
    this.autoOpenChat();
    this.showInitialGreeting();
  }

  autoOpenChat() {
    // Auto-open the chat window after 2 seconds
    setTimeout(() => {
      this.isOpen = true;
      const chatWindow = document.getElementById("chat-window");
      const toggleBtn = document.getElementById("chat-toggle");
      if (chatWindow && toggleBtn) {
        chatWindow.classList.add("open");
        toggleBtn.innerHTML = '✕';
      }
    }, 2000);
  }

  detectPage() {
    const path = window.location.pathname;
    if (path.includes("splash")) return "splash";
    if (path.includes("about")) return "about";
    if (path.includes("ongoing")) return "ongoing";
    if (path.includes("artwork")) return "artwork";
    if (path.includes("tech")) return "tech";
    if (path.includes("services")) return "services";
    return "general";
  }

  createChatBubble() {
    // Create container
    const bubble = document.createElement("div");
    bubble.id = "freddy-chat-bubble";
    bubble.innerHTML = `
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap');

        @font-face {
          font-family: 'Courier Prime';
        }

        #freddy-chat-bubble {
          position: fixed;
          bottom: 20px;
          right: 20px;
          z-index: 100000;
          font-family:'Courier Prime', monospace;
          font-size: 14px;
        }

        .chat-toggle-btn {
          width: 60px;
          height: 60px;
          border-radius: 0;
          background: #FFDD00;
          border: 3px solid #000;
          color: #000;
          font-size: 28px;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s ease;
          font-weight: bold;
          box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.3);
        }

        .chat-toggle-btn:hover {
          transform: translate(-2px, -2px);
          box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.3);
        }

        .chat-toggle-btn:active {
          transform: translate(2px, 2px);
          box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.3);
        }

        .chat-window {
          display: none;
          position: absolute;
          bottom: 80px;
          right: 0;
          width: 350px;
          height: 500px;
          background: #000;
          border: 2px solid #00ff00;
          border-radius: 8px;
          box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
          flex-direction: column;
          overflow: hidden;
          animation: slideUp 0.3s ease;
        }

        .chat-window.open {
          display: flex;
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .chat-header {
          background: #000;
          color: #00ff00;
          padding: 12px;
          font-weight: bold;
          text-align: center;
          border-bottom: 2px solid #00ff00;
          font-family: 'Courier Prime', monospace;
          font-size: 16px;
        }

        .chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 12px;
          background: #000;
          color: #00ff00;
          scrollbar-width: thin;
          scrollbar-color: #00ff00 #111;
        }

        .chat-messages::-webkit-scrollbar {
          width: 8px;
        }

        .chat-messages::-webkit-scrollbar-track {
          background: #111;
        }

        .chat-messages::-webkit-scrollbar-thumb {
          background: #00ff00;
          border-radius: 4px;
        }

        .message {
          margin-bottom: 12px;
          line-height: 1.4;
          word-wrap: break-word;
          font-family: 'Courier Prime', monospace;
          font-size: 13px;
        }

        .message.user {
          color: #00ff00;
          text-align: right;
          margin-left: 20px;
        }

        .message.user::before {
          content: "> ";
          color: #00aa00;
        }

        .message.bot {
          color: #00ffff;
          margin-right: 20px;
        }

        .message.bot::before {
          content: "[FREDDY] ";
          color: #00ff00;
          font-weight: bold;
        }

        .typing-indicator {
          display: flex;
          gap: 4px;
          color: #00ff00;
          font-size: 12px;
        }

        .typing-indicator span {
          animation: blink 1.4s infinite;
        }

        .typing-indicator span:nth-child(2) {
          animation-delay: 0.2s;
        }

        .typing-indicator span:nth-child(3) {
          animation-delay: 0.4s;
        }

        @keyframes blink {
          0%, 60%, 100% {
            opacity: 0.5;
          }
          30% {
            opacity: 1;
          }
        }

        .chat-input-area {
          display: flex;
          gap: 6px;
          padding: 10px;
          border-top: 2px solid #00ff00;
          background: #000;
        }

        .chat-input {
          flex: 1;
          background: #111;
          border: 1px solid #00ff00;
          color: #00ff00;
          padding: 8px;
          font-family: 'Courier Prime', monospace;
          font-size: 13px;
          outline: none;
        }

        .chat-input::placeholder {
          color: #006600;
        }

        .chat-input:focus {
          box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
        }

        .send-btn {
          background: #00ff00;
          border: none;
          color: #000;
          padding: 8px 12px;
          cursor: pointer;
          font-weight: bold;
          border-radius: 4px;
          transition: all 0.2s;
        }

        .send-btn:hover {
          background: #00aa00;
          box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        }

        .send-btn:active {
          transform: scale(0.95);
        }

        /* Cursor blink effect */
        .cursor {
          display: inline-block;
          width: 2px;
          height: 1em;
          background: #00ff00;
          margin-left: 2px;
          animation: cursorBlink 1s infinite;
        }

        @keyframes cursorBlink {
          0%, 49% {
            background: #00ff00;
          }
          50%, 100% {
            background: transparent;
          }
        }
      </style>

      <button class="chat-toggle-btn" id="chat-toggle">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="2" y="4" width="22" height="18" rx="2" fill="#000"/>
          <path d="M10 14H22" stroke="#000" stroke-width="1" stroke-linecap="round"/>
          <path d="M10 10H20" stroke="#000" stroke-width="1" stroke-linecap="round"/>
          <path d="M10 18H16" stroke="#000" stroke-width="1" stroke-linecap="round"/>
          <polygon points="24,22 24,28 30,28 24,22" fill="#000"/>
        </svg>
      </button>
      
      <div class="chat-window" id="chat-window">
        <div class="chat-header">
          Non-GMO Clone at your service <span class="cursor"></span>
        </div>
        <div class="chat-messages" id="chat-messages"></div>
        <div class="chat-input-area">
          <input 
            type="text" 
            class="chat-input" 
            id="chat-input" 
            placeholder="type here..."
            autocomplete="off"
          >
          <button class="send-btn" id="send-btn">→</button>
        </div>
      </div>
    `;

    document.body.appendChild(bubble);
  }

  attachEventListeners() {
    const toggleBtn = document.getElementById("chat-toggle");
    const sendBtn = document.getElementById("send-btn");
    const chatInput = document.getElementById("chat-input");
    const chatWindow = document.getElementById("chat-window");

    toggleBtn.addEventListener("click", () => this.toggleChat());
    sendBtn.addEventListener("click", () => this.sendMessage());
    chatInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") this.sendMessage();
    });

    // Close chat when clicking outside (optional)
    document.addEventListener("click", (e) => {
      if (
        !chatWindow.contains(e.target) &&
        !toggleBtn.contains(e.target) &&
        this.isOpen
      ) {
        // Uncomment to auto-close:
        // this.toggleChat();
      }
    });
  }

  toggleChat() {
    this.isOpen = !this.isOpen;
    const chatWindow = document.getElementById("chat-window");
    const toggleBtn = document.getElementById("chat-toggle");

    if (this.isOpen) {
      chatWindow.classList.add("open");
      document.getElementById("chat-input").focus();
      toggleBtn.innerHTML = '✕';
    } else {
      chatWindow.classList.remove("open");
      toggleBtn.innerHTML = `
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="2" y="4" width="22" height="18" rx="2" fill="#000"/>
          <path d="M10 14H22" stroke="#000" stroke-width="1" stroke-linecap="round"/>
          <path d="M10 10H20" stroke="#000" stroke-width="1" stroke-linecap="round"/>
          <path d="M10 18H16" stroke="#000" stroke-width="1" stroke-linecap="round"/>
          <polygon points="24,22 24,28 30,28 24,22" fill="#000"/>
        </svg>
      `;
    }
  }

  showInitialGreeting() {
    setTimeout(() => {
      const greetings = {
        splash: "hello? someone there?",
        about: "curious about freddy's work?",
        ongoing: "check out what's cooking...",
        artwork: "art in progress...",
        tech: "nerding out on code...",
        services: "ready to collaborate?",
        general: "hello? someone there?"
      };

      const greeting = greetings[this.currentPage] || "hello?";
      this.addMessage(greeting, "bot");
    }, 1000);
  }

  async sendMessage() {
    const input = document.getElementById("chat-input");
    const message = input.value.trim();

    if (!message) return;

    // Add user message to chat
    this.addMessage(message, "user");
    input.value = "";

    // Show typing indicator
    this.addTypingIndicator();

    try {
      const response = await fetch(this.apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: message,
          page_context: this.currentPage
        })
      });

      if (!response.ok) throw new Error("API error");

      const data = await response.json();
      this.removeTypingIndicator();
      this.addMessage(data.reply, "bot");
    } catch (error) {
      this.removeTypingIndicator();
      console.error("Chat error:", error);
      this.addMessage(
        "ERROR: connection lost | try again later",
        "bot"
      );
    }
  }

  addMessage(text, sender) {
    const messagesDiv = document.getElementById("chat-messages");
    const messageEl = document.createElement("div");
    messageEl.className = `message ${sender}`;
    messageEl.textContent = text;

    messagesDiv.appendChild(messageEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  addTypingIndicator() {
    const messagesDiv = document.getElementById("chat-messages");
    const typingEl = document.createElement("div");
    typingEl.className = "typing-indicator";
    typingEl.id = "typing-indicator";
    typingEl.innerHTML = "<span>.</span><span>.</span><span>.</span>";

    messagesDiv.appendChild(typingEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  removeTypingIndicator() {
    const typing = document.getElementById("typing-indicator");
    if (typing) typing.remove();
  }
}

// Initialize chatbot when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    new FreddyChatbot();
  });
} else {
  new FreddyChatbot();
}
