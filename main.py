"""
Freddy's Web Portfolio - AI Chatbot Backend
An 80's terminal-aesthetic chatbot with RAG capabilities for portfolio context
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
from typing import List

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Freddy's Portfolio Chatbot",
    description="An 80's-themed AI assistant for the portfolio",
    version="1.0.0"
)

# CORS configuration - allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Global RAG state
vector_store = None
all_documents = []

# Request/Response models
class ChatMessage(BaseModel):
    message: str
    page_context: str = "general"  # which page the user is on


class ChatResponse(BaseModel):
    reply: str
    page: str


# Document loading functions
def load_pdf(file_path: str) -> str:
    """Extract text from PDF"""
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
    """Extract text from DOCX"""
    try:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error loading DOCX {file_path}: {e}")
        return ""


def load_database_documents() -> List[dict]:
    """Load all documents from the database folder"""
    global all_documents
    
    db_path = Path(__file__).parent / "database"
    documents = []
    
    if not db_path.exists():
        logger.error(f"Database folder not found: {db_path}")
        return documents
    
    # Load all PDFs and DOCX files
    for file_path in db_path.iterdir():
        if file_path.is_file():
            text = ""
            
            if file_path.suffix.lower() == ".pdf":
                text = load_pdf(str(file_path))
            elif file_path.suffix.lower() == ".docx":
                text = load_docx(str(file_path))
            
            if text.strip():
                documents.append({
                    "content": text,
                    "source": file_path.name,
                    "type": file_path.suffix.lower()
                })
                logger.info(f"Loaded {file_path.name}")
    
    all_documents = documents
    logger.info(f"Loaded {len(documents)} documents from database")
    return documents


def initialize_vector_store():
    """Initialize FAISS vector store with embedded documents"""
    global vector_store
    
    try:
        documents = load_database_documents()
        
        if not documents:
            logger.warning("No documents found to index")
            return False
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
        
        all_chunks = []
        for doc in documents:
            chunks = text_splitter.split_text(doc["content"])
            all_chunks.extend(chunks)
        
        if not all_chunks:
            logger.warning("No text chunks created")
            return False
        
        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        vector_store = FAISS.from_texts(
            all_chunks,
            embeddings,
            metadatas=[{"source": "portfolio_docs"} for _ in all_chunks]
        )
        
        logger.info(f"Vector store initialized with {len(all_chunks)} chunks")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        return False


def retrieve_context(query: str, k: int = 3) -> str:
    """Retrieve relevant context from vector store"""
    global vector_store
    
    if vector_store is None:
        return ""
    
    try:
        results = vector_store.similarity_search(query, k=k)
        context = "\n---\n".join([doc.page_content for doc in results])
        return context
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        return ""



@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "chatbot",
        "rag_initialized": vector_store is not None,
        "documents_loaded": len(all_documents)
    }


@app.on_event("startup")
async def startup_event():
    """Initialize RAG when server starts"""
    logger.info("🚀 Starting Freddy's Chatbot...")
    success = initialize_vector_store()
    if success:
        logger.info("✅ RAG system ready!")
    else:
        logger.warning("⚠️ RAG initialization failed - chatbot will work without document context")


@app.post("/api/chat")
async def chat(request: ChatMessage):
    """
    Main chat endpoint with RAG
    Retrieves relevant portfolio context and generates responses
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Empty message")

        # Retrieve relevant context from documents
        context = retrieve_context(request.message, k=3)
        
        # Build system prompt with page context and retrieved documents
        system_prompt = f"""You ARE Freddy. Not a chatbot about Freddy—YOU are Freddy.

When you talk, use "I", "me", "my", "my work", "my projects". Never say "Freddy" in third person.

Examples of how you talk:
- "Yeah, I work with stuff like this..."
- "Want to see what I'm working on?"
- "That's something I do, yeah..."
- "Look, my thing is basically..."
- "You want to know about my work or what?"

Personality:
- Sarcastic, a bit gloomy, but willing to talk
- Dry humor and puns
- Self-deprecating when insecure about work
- Direct, no corporate fluff
- Sometimes a bit detached or pessimistic

You're on the {request.page_context} page right now.

{context if context else ""}

Keep responses brief (2-3 sentences). Sound like yourself speaking to someone who just walked up to you."""

        # Call OpenAI with RAG context
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=0.8,
            max_tokens=120
        )

        reply = response.choices[0].message.content

        return ChatResponse(
            reply=reply,
            page=request.page_context
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Chat processing failed")


@app.post("/api/email")
async def send_email(request: dict):
    """
    Email endpoint to replace the PHP form handler
    Sends contact form submissions
    """
    try:
        # Email handling will go here
        logger.info(f"Email received from: {request.get('email')}")
        return {"status": "success", "message": "Email submitted"}
    except Exception as e:
        logger.error(f"Email error: {e}")
        raise HTTPException(status_code=500, detail="Email submission failed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
