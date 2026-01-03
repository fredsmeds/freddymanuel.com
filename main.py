"""
Freddy's Web Portfolio - AI Chatbot Backend
Version 1.17.0 (Cloud Deployment)
- Feature: Added Contact Form Emailer (Replaces PHP).
- Preserved: Multilingual greetings, Personas, and Advanced Search Logic.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging
from openai import OpenAI
from pathlib import Path
from pypdf import PdfReader
from docx import Document
import faiss
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional, Dict
import re
import unicodedata

# --- NEW IMPORTS FOR EMAIL ---
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

# --- CUSTOM LOGGING FORMAT ---
class BrainLogger(logging.Logger):
    def think(self, msg):
        self.info(f"\n🧠 THOUGHT: {msg}")
    def search(self, msg):
        self.info(f"🔍 SEARCH: {msg}")
    def found(self, msg):
        self.info(f"📄 FOUND: {msg}")
    def nav(self, msg):
        self.info(f"🧭 NAVIGATION: {msg}\n")

logging.setLoggerClass(BrainLogger)
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("freddy_brain")

app = FastAPI(title="Freddy's Portfolio Chatbot", version="1.17.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow Cloudflare to access this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- GLOBAL VARIABLES ---
vector_store = None
all_documents = []

# --- MULTILINGUAL GREETINGS (PRESERVED) ---
PAGE_GREETINGS = {
    "about": {
        "en": [
            "Uff, the awkward part where you sell yourself huh?",
            "Of course you can ask me stuff too, but this page here took me some work so read through it.",
            "I'll be here for any questions."
        ],
        "es": [
            "O sea, qué ladilla hablar de uno mismo, ¿no?",
            "Esta página me presenta un pelo. Léela ahí, chamo. Estoy pendiente por si tienes dudas."
        ],
        "pt": [
            "Aquela cena constrangedora de 'vender o peixe', tás a ver?",
            "A página explica quem sou. Se tiveres dúvidas, apita."
        ]
    },
    "ongoing": {
        "en": ["Ah this part is exciting, the projects I'm developing right now.", "Check it out, I'm still here."],
        "es": ["Epa, esto está candela. Lo que estoy cocinando ahorita.", "Mosca ahí, que sigo aquí pendiente."],
        "pt": ["Ya, isto é o que estou a fazer agora.", "Vê lá isso, estou por aqui."]
    },
    "artwork": {
        "en": ["Ok this is like a hand-picked collection of my most valuable achievements.", "Very proud of these babies."],
        "es": ["Ok, esto es tipo la joya de la corona, o sea, mis logros.", "Burda de orgulloso de estos bebés, valecito."],
        "pt": ["Tipo, é uma coleção escolhida a dedo.", "Tenho bué orgulho nisto, sinceramente."]
    },
    "tech": {
        "en": ["This is the part with the technicities.", "If you're curious to know....you know... here."],
        "es": ["Aquí está la parte técnica, pura ingeniería y vaina.", "Si te pica la curiosidad... dale."],
        "pt": ["A parte técnica. Se fores nerd e quiseres saber como funciona... é aqui."]
    },
    "services": {
        "en": ["Here's some details of what brings the bread to my table.", "Let's get our hands dirty - what do you wanna build?"],
        "es": ["Aquí es donde se factura (pa' pagar Amazon) mientras se goza creando.", "A ver, chamo, ¿qué vamos a montar?"],
        "pt": ["É isto que mete pão na mesa (e cenas da Amazon).", "Vamos meter as mãos na massa - o que queres construir?"]
    }
}

# --- DATA MODELS ---
class ChatMessage(BaseModel):
    message: str
    page_context: str = "general"

class ChatResponse(BaseModel):
    reply: List[str] 
    page: str
    navigation_target: Optional[str] = None
    detected_language: Optional[str] = "en"

# --- NEW CONTACT FORM MODEL ---
class ContactForm(BaseModel):
    name: str
    email: str 
    phone: Optional[str] = "Not provided"
    project_type: Optional[str] = "General"
    message: str

# --- NEW EMAIL FUNCTION ---
def send_email_notification(data: ContactForm):
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_PASSWORD")
    
    if not gmail_user or not gmail_pass:
        logger.error("❌ Gmail credentials not set in environment variables.")
        return False

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = gmail_user # Send to yourself
    msg['Subject'] = f"🚀 New Portfolio Lead: {data.name}"
    msg['Reply-To'] = data.email

    body = f"""
    New contact from FreddyManuel.com:
    
    👤 Name: {data.name}
    📧 Email: {data.email}
    📱 Phone: {data.phone}
    🏗️ Project: {data.project_type}
    
    📝 Message:
    {data.message}
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_pass)
        server.send_message(msg)
        server.quit()
        logger.info(f"✅ Email sent for {data.name}")
        return True
    except Exception as e:
        logger.error(f"❌ Email failed: {e}")
        return False

# --- DOCUMENT LOADING FUNCTIONS (PRESERVED) ---
def load_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error loading PDF {file_path}: {e}")
        return ""

def load_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error loading DOCX {file_path}: {e}")
        return ""

def load_text(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if file_path.endswith(".html"):
            content = re.sub(r'<(script|style).*?>.*?</\1>', '', content, flags=re.DOTALL)
            content = re.sub(r'<[^>]+>', ' ', content)
            content = re.sub(r'\s+', ' ', content).strip()
        return content
    except Exception as e:
        logger.error(f"Error loading text file {file_path}: {e}")
        return ""

def load_database_documents() -> List[dict]:
    global all_documents
    db_path = Path(__file__).parent / "database"
    root_path = Path(__file__).parent 
    documents = []
    
    # 1. Load index.html
    index_file = root_path / "index.html"
    if index_file.exists():
        text = load_text(str(index_file))
        if text:
            documents.append({"content": text, "source": "index.html", "type": "website_content"})
            logger.info("Loaded index.html as website_content")

    # 2. Load Database Files
    if db_path.exists():
        for file_path in db_path.iterdir():
            if file_path.is_file():
                text = ""
                fname = file_path.name.lower()
                
                if file_path.suffix.lower() == ".pdf": text = load_pdf(str(file_path))
                elif file_path.suffix.lower() == ".docx": text = load_docx(str(file_path))
                elif file_path.suffix.lower() in [".md", ".txt", ".html"]: text = load_text(str(file_path))
                
                if text.strip():
                    if "psyche" in fname:
                        doc_type = "personal_philosophy" 
                    elif "portfolio" in fname:
                        doc_type = "work_technical" 
                    elif "behaviour" in fname:
                        doc_type = "persona_instructions"
                    elif file_path.suffix.lower() == ".md" or "readme" in fname:
                        doc_type = "technical_docs" 
                    else:
                        doc_type = "general_content" 
                    
                    documents.append({
                        "content": text,
                        "source": file_path.name,
                        "type": doc_type
                    })
                    logger.info(f"Loaded {file_path.name} as {doc_type}")
    
    all_documents = documents
    return documents

def initialize_vector_store():
    global vector_store
    try:
        documents = load_database_documents()
        if not documents: return False
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        all_chunks = []
        metadatas = []
        
        for doc in documents:
            chunks = text_splitter.split_text(doc["content"])
            all_chunks.extend(chunks)
            metadatas.extend([{"source": doc["source"], "type": doc["type"]} for _ in chunks])
        
        if not all_chunks: return False
        
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        vector_store = FAISS.from_texts(texts=all_chunks, embedding=embeddings, metadatas=metadatas)
        
        logger.info(f"✅ RAG Ready: {len(all_chunks)} chunks indexed.")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        return False

# --- INTELLIGENT RETRIEVAL LOGIC (PRESERVED) ---
def generate_search_variations(query: str) -> List[str]:
    variations = []
    q_lower = query.lower()
    
    # 1. Keyword Injection
    personal_keywords = ["story", "history", "life", "bio", "background", "personal", "who are you", "quien eres", "historia", "vida", "debord", "spectacle", "philosophy"]
    if any(k in q_lower for k in personal_keywords):
        variations.append("Freddy's personal biography childhood dreams and Guy Debord philosophy from freddy_psyche.pdf")

    tech_keywords = ["job", "career", "cv", "resume", "experience", "hiring", "skills", "tech stack", "technologies", "el primo", "masto", "olympian", "code", "built", "engineering", "art", "video", "project", "work", "trabajo", "tecnico"]
    if any(k in q_lower for k in tech_keywords):
        variations.append("Technical projects engineering skills and artwork details from portfolio.pdf")

    if "el primo" in q_lower: variations.append("El Primo Cleaning Products technical details in portfolio.pdf")
    if "masto" in q_lower: variations.append("Masto Inc technical details in portfolio.pdf")
    if "olympian" in q_lower: variations.append("Olympian Power Cleaners technical details in portfolio.pdf")
    if "yum" in q_lower or "video" in q_lower: variations.append("YUM video installation description index.html")

    # 2. Strict LLM Generation
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a database search assistant. Output ONLY 2 search queries based on the user's input. Do NOT answer the user. Do NOT be conversational. Just output the queries."},
                {"role": "user", "content": f"User input: {query}"}
            ],
            temperature=0.3 # Low temp to stop chatting
        )
        llm_vars = response.choices[0].message.content.strip().split('\n')
        variations.extend([v.strip() for v in llm_vars if v.strip()])
    except:
        variations.append(query)

    return list(set(variations))

def retrieve_context(query: str) -> str:
    global vector_store
    if vector_store is None: return ""
    variations = generate_search_variations(query)
    logger.think(f"Search Queries: {variations}")
    unique_docs = {}
    for q in variations:
        results = vector_store.similarity_search(q, k=4) 
        for doc in results:
            if doc.page_content not in unique_docs: unique_docs[doc.page_content] = doc
    final_docs = list(unique_docs.values())[:10] 
    context_str = ""
    for i, doc in enumerate(final_docs):
        src = doc.metadata.get('source', 'unknown')
        dtype = doc.metadata.get('type', 'unknown') 
        snippet = doc.page_content[:100].replace('\n', ' ') + "..."
        context_str += f"[Source: {src} | Type: {dtype}] {doc.page_content}\n\n"
        logger.found(f"Doc {i+1} ({src}): {snippet}")
    return context_str

def split_into_sentences(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def normalize_text(text: str) -> str:
    """Removes accents and lowercase: 'Técnicos' -> 'tecnicos'"""
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn").lower()

def detect_project_redirect(message: str) -> Optional[str]:
    msg = normalize_text(message)
    
    # Artwork / Art
    if any(x in msg for x in ["yum", "internercia", "park", "nepal", "cosmo", "art", "arte", "artistico"]): 
        return "artwork"
    
    # Tech / Web / Engineering (EXPANDED KEYWORDS)
    if any(x in msg for x in ["diaries", "zelda", "olympian", "masto", "el primo", "cleaning", "tech", "tecnologia", "tecnico", "trabajo tecnico", "web", "desarrollo", "codigo", "programacion", "ingenieria"]): 
        return "tech"
        
    # Ongoing
    if any(x in msg for x in ["coro", "ongoing", "proyectos", "cocinando"]): 
        return "ongoing"
        
    # Services
    if any(x in msg for x in ["hire", "service", "build", "servicios", "contratar", "facturar"]): 
        return "services"
        
    return None

# --- ENDPOINTS ---

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting Freddy's Chatbot...")
    initialize_vector_store()

@app.get("/")
def home():
    return {"status": "online", "message": "Freddy's Brain is Running"}

@app.get("/api/welcome/{page}")
async def get_page_welcome(page: str, lang: str = "en"):
    logger.nav(f"User arrived at: {page} (Language: {lang})")
    if lang not in ["en", "es", "pt"]: lang = "en"

    if page == "splash":
        return {"type": "sequence", "messages": [
            {"text": "Who's there?", "delay": 2000},
            {"text": "Who are you, what do you want from me?", "delay": 1000},
            {"text": "I HAVE A KNIFE! Lol", "delay": 0}
        ]}
    if page in PAGE_GREETINGS:
        text_list = PAGE_GREETINGS[page].get(lang, PAGE_GREETINGS[page]["en"])
        msgs = [{"text": txt, "delay": 1200} for txt in text_list]
        return {"type": "standard", "messages": msgs}
        
    return {"type": "standard", "messages": [{"text": "So, what's up?", "delay": 0}]}

@app.post("/api/chat")
async def chat(request: ChatMessage):
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Empty message")

        logger.think(f"User Message: '{request.message}' | Page: {request.page_context}")
        context = retrieve_context(request.message)
        
        smart_redirect = detect_project_redirect(request.message)
        redirect_instruction = ""
        if smart_redirect:
            redirect_instruction = f"URGENT: User is asking about '{smart_redirect}' content. You MUST redirect them using ||REDIRECT:{smart_redirect}|| at the end."

        # --- SYSTEM PROMPT ---
        system_prompt = f"""
You are Freddy, a 38-year-old multimedia artist and AI engineer.
Current Page: {request.page_context}

**CORE TASK:**
1. Detect user language (En, Es, Pt).
2. Adopt PERSONA.
3. **IMPORTANT:** End response with ||LANG:xx||.

**PERSONAS:**
🟢 **ENGLISH:** Dark humor, dry sarcasm. "Beautifully Horrendous" taste. Punchy.
🟡 **SPANISH (VENEZUELAN):** "MILF sifrina" + "Caracas Millennial". Vocab: "O sea, valecito" + "chamo, mosca". Tono: Condescendiente pero útil.
🔵 **PORTUGUESE (PT-PT):** Millennial Tuga. Serio, inseguro, técnico. Vocab: "ya, bué, tipo, tás a ver".

**REFUSAL:** If not En/Es/Pt, reply with standard English "Non-GMO clone" refusal.

**PRIVACY:** No sexuality unless asked. If asked: "Yes, I like dick. Did that help? Next question." (Translate).

**NAVIGATION:**
{redirect_instruction}
1. **CLEAR REQUEST:** Redirect IMMEDIATELY (||REDIRECT:page||).
2. **VAGUE REQUEST:** Banter first.

**CONTEXT:**
{context}

**INSTRUCTIONS:**
- Use [Source: portfolio.pdf] for work/tech.
- Use [Source: freddy_psyche.pdf] for personal/philosophy.
- Be punchy.
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=0.85,
            max_tokens=350
        )

        full_reply = response.choices[0].message.content
        
        detected_lang = "en"
        if "||LANG:" in full_reply:
            parts = full_reply.split("||LANG:")
            full_reply = parts[0].strip()
            detected_lang = parts[1].strip()[:2].lower()
            logger.think(f"Detected Language: {detected_lang}")

        nav_target = None
        if "||REDIRECT:" in full_reply:
            parts = full_reply.split("||REDIRECT:")
            full_reply = parts[0].strip()
            raw_target = parts[1].strip().lower()
            valid_pages = ["about", "ongoing", "artwork", "tech", "services", "splash"]
            for page in valid_pages:
                if page in raw_target:
                    nav_target = page
                    break
            if not nav_target: nav_target = re.sub(r'[^a-z]', '', raw_target)
            logger.nav(f"Redirecting user to: {nav_target}")

        split_replies = split_into_sentences(full_reply)

        return ChatResponse(
            reply=split_replies, 
            page=request.page_context,
            navigation_target=nav_target,
            detected_language=detected_lang
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Chat processing failed")

# --- NEW CONTACT ENDPOINT ---
@app.post("/api/contact")
async def submit_contact_form(form: ContactForm):
    logger.info(f"📨 Contact Form received from {form.name}")
    
    # Map 'other' or codes to readable text
    project_map = {
        "ai-ml": "AI & Machine Learning",
        "web-dev": "Web Development",
        "branding": "Branding Strategy",
        "creative-production": "Creative Production"
    }
    form.project_type = project_map.get(form.project_type, form.project_type)

    success = send_email_notification(form)
    
    if success:
        return {"success": True, "message": "Message sent! Freddy will contact you soon."}
    else:
        # Return success=False to let frontend handle the error UI
        return {"success": False, "message": "Server email error. Please email fmroldanrivero@gmail.com directly."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")