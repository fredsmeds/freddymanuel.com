/**
 * Freddy's Portfolio Chatbot
 * Version: 1.7.6
 * Features:
 * - Active Navigation Handling (Simulates clicks for SPA)
 * - Anti-duplication logic
 * - Style Update: Neon Yellow (#F9FF25) + SVG Icon
 */

class FreddyChatbot {
    constructor() {
      this.isOpen = false;
      this.messages = [];
      this.currentPage = this.detectPage();
      this.isNavigating = false; 
      this.lastGreetingTime = 0;
      this.currentLanguage = "en"; 
      
      this.apiUrl = "https://freddy-backend.onrender.com/api"; // (Use your REAL Render URL)
      
      // Define the SVG icon constant for reuse
      this.chatIconSVG = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="black">
          <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
        </svg>
      `;

      this.init();
    }
  
    init() {
      this.createChatBubble();
      this.attachEventListeners();
      this.autoOpenChat();
      this.triggerWelcomeSequence();
    }
  
    detectPage() {
      const splash = document.getElementById("splash-screen");
      if (splash && !splash.classList.contains("hidden") && getComputedStyle(splash).display !== "none") {
          return "splash";
      }
      const path = window.location.pathname.toLowerCase();
      if (path.includes("about")) return "about";
      if (path.includes("ongoing")) return "ongoing";
      if (path.includes("artwork")) return "artwork";
      if (path.includes("tech")) return "tech";
      if (path.includes("services")) return "services";
      return "about"; 
    }
  
    autoOpenChat() {
      setTimeout(() => {
        this.isOpen = true;
        const chatWindow = document.getElementById("chat-window");
        const toggleBtn = document.getElementById("chat-toggle");
        if (chatWindow && toggleBtn) {
          chatWindow.classList.add("open");
          toggleBtn.innerText = '✕';
        }
      }, 1500);
    }
  
    async triggerWelcomeSequence() {
      const now = Date.now();
      if (now - this.lastGreetingTime < 2000) return;
      this.lastGreetingTime = now;

      try {
        console.log(`fetching greeting for: ${this.currentPage} (Lang: ${this.currentLanguage})`);
        
        const response = await fetch(`${this.apiUrl}/welcome/${this.currentPage}?lang=${this.currentLanguage}`);
        
        if (!response.ok) throw new Error("Welcome API failed");
        
        const data = await response.json();
        const messages = data.messages;
  
        let cumulativeDelay = 1000; 
        for (const msg of messages) {
          setTimeout(() => {
            this.addMessage(msg.text, "bot");
          }, cumulativeDelay);
          cumulativeDelay += (msg.delay !== undefined ? msg.delay : 1000); 
        }
      } catch (error) {
        console.error("Welcome sequence error:", error);
      }
    }
  
    async sendMessage() {
      const input = document.getElementById("chat-input");
      const message = input.value.trim();
      if (!message) return;
  
      this.addMessage(message, "user");
      input.value = "";
      this.addTypingIndicator();
  
      try {
        const response = await fetch(`${this.apiUrl}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: message,
            page_context: this.currentPage
          })
        });
  
        if (!response.ok) throw new Error("API error");
  
        const data = await response.json();
        this.removeTypingIndicator();

        if (data.detected_language) {
            this.currentLanguage = data.detected_language;
        }
  
        if (Array.isArray(data.reply)) {
            for (const msg of data.reply) {
                this.addMessage(msg, "bot");
                await new Promise(r => setTimeout(r, 500 + Math.random() * 400));
            }
        } else {
            this.addMessage(data.reply, "bot");
        }

        if (data.navigation_target) {
            console.log("Navigating to:", data.navigation_target);
            setTimeout(() => {
                this.handleNavigation(data.navigation_target);
            }, 1000); 
        }
  
      } catch (error) {
        this.removeTypingIndicator();
        console.error("Chat error:", error);
        this.addMessage("...glitch in the matrix...", "bot");
      }
    }

    handleNavigation(targetPage) {
        this.addMessage(`🔄 warping to ${targetPage}...`, "bot");
        this.isNavigating = true;

        if (this.currentPage === "splash" && targetPage !== "splash") {
            const enterBtn = document.getElementById("enter-btn");
            if (enterBtn) {
                console.log("🤖 Chatbot clicking Enter...");
                enterBtn.click();
                setTimeout(() => this.executeSectionSwitch(targetPage), 500);
            } else {
                this.executeSectionSwitch(targetPage);
            }
        } else {
            this.executeSectionSwitch(targetPage);
        }
    }

    executeSectionSwitch(targetPage) {
        const navBtn = document.querySelector(`.nav-item[data-page="${targetPage}"]`);
        if (navBtn) {
            navBtn.click(); 
        } else {
            console.warn(`Could not find nav button for: ${targetPage}`);
            this.isNavigating = false; 
        }
    }
  
    addMessage(text, sender) {
      const messagesDiv = document.getElementById("chat-messages");
      if(!messagesDiv) return;
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
      typingEl.innerText = "typing...";
      messagesDiv.appendChild(typingEl);
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
  
    removeTypingIndicator() {
      const typing = document.getElementById("typing-indicator");
      if (typing) typing.remove();
    }
  
    createChatBubble() {
      const bubble = document.createElement("div");
      bubble.id = "freddy-chat-bubble";
      bubble.innerHTML = `
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap');
  
          #freddy-chat-bubble {
            position: fixed; bottom: 20px; right: 20px; z-index: 100000;
            font-family:'Courier Prime', monospace; font-size: 14px;
          }
  
          .chat-toggle-btn {
            width: 60px; height: 60px;
            background: #F9FF25; /* UPDATED COLOR */
            border: 3px solid #000;
            color: #000; 
            font-size: 28px; 
            cursor: pointer; 
            display: flex; align-items: center; justify-content: center; 
            box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.3); 
            transition: all 0.2s;
          }
          .chat-toggle-btn:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0 rgba(0,0,0,0.3); }
          .chat-toggle-btn:active { transform: translate(2px, 2px); box-shadow: 2px 2px 0 rgba(0,0,0,0.3); }
  
          .chat-window {
            display: none; position: absolute; bottom: 80px; right: 0;
            width: 350px; height: 500px;
            background: #000; border: 2px solid #00ff00;
            border-radius: 8px; box-shadow: 0 0 30px rgba(0, 255, 0, 0.2);
            flex-direction: column; overflow: hidden;
            animation: slideUp 0.3s ease;
          }
          .chat-window.open { display: flex; }
          @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
  
          .chat-header {
            background: #000; color: #00ff00; padding: 12px; text-align: center; border-bottom: 2px solid #00ff00; font-weight: bold;
          }
  
          .chat-messages {
            flex: 1; overflow-y: auto; padding: 15px;
            background: #000; color: #00ff00;
            scrollbar-width: thin; scrollbar-color: #00ff00 #111;
          }
  
          .message { margin-bottom: 12px; max-width: 90%; word-wrap: break-word; }
          
          .message.user {
            color: #F9FF25; /* UPDATED COLOR */
            text-align: right; margin-left: auto;
          }
          .message.user::before { content: "> "; color: #F9FF25; } /* UPDATED COLOR */
  
          .message.bot { color: #00ff00; text-align: left; margin-right: auto; }
          .message.bot::before { content: "[FREDDY] "; color: #00aa00; font-size: 0.8em; }
  
          .chat-input-area { display: flex; gap: 6px; padding: 10px; border-top: 2px solid #00ff00; background: #000; }
          .chat-input { flex: 1; background: #111; border: 1px solid #00ff00; color: #00ff00; padding: 8px; font-family: 'Courier Prime', monospace; outline: none; }
          .send-btn { background: #00ff00; border: none; color: #000; padding: 8px 15px; cursor: pointer; font-weight: bold; }
        </style>
        
        <button class="chat-toggle-btn" id="chat-toggle">
            ${this.chatIconSVG}
        </button>
        
        <div class="chat-window" id="chat-window">
          <div class="chat-header">
            Non-GMO Clone <span class="cursor"></span>
          </div>
          <div class="chat-messages" id="chat-messages"></div>
          <div class="chat-input-area">
            <input type="text" class="chat-input" id="chat-input" placeholder="Say something..." autocomplete="off">
            <button class="send-btn" id="send-btn">SEND</button>
          </div>
        </div>
      `;
      document.body.appendChild(bubble);
    }
  
    attachEventListeners() {
      const toggleBtn = document.getElementById("chat-toggle");
      const sendBtn = document.getElementById("send-btn");
      const chatInput = document.getElementById("chat-input");
  
      toggleBtn.addEventListener("click", () => {
          this.isOpen = !this.isOpen;
          const win = document.getElementById("chat-window");
          if(this.isOpen) { 
              win.classList.add("open"); 
              toggleBtn.innerText = '✕'; // Keep X for close
              document.getElementById("chat-input").focus();
          } else { 
              win.classList.remove("open"); 
              toggleBtn.innerHTML = this.chatIconSVG; // Restore SVG icon
          }
      });
  
      sendBtn.addEventListener("click", () => this.sendMessage());
      chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") this.sendMessage();
      });

      document.querySelectorAll('.nav-item').forEach(item => {
          item.addEventListener('click', (e) => {
              if (this.isNavigating) return;
              const page = item.getAttribute('data-page');
              if (page && page !== this.currentPage) {
                  this.currentPage = page;
                  setTimeout(() => { this.triggerWelcomeSequence(); }, 1500);
              }
          });
      });
    }
  }
  
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => new FreddyChatbot());
  } else {
    new FreddyChatbot();
  }