import os
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Setup Logging (Shows professionalism in portfolios)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Load env vars (INFERENCE_SERVER_URL)
load_dotenv()

def ingest_docs(data_folder="./data", db_folder="./vector_db"):
    """
    Loads PDFs, chunks them, and stores them in ChromaDB 
    using the inference server for embedding calculations.
    """
    inference_server_ip = os.getenv("INFERENCE_SERVER_IP")
    if not inference_server_ip:
        logger.error("INFERENCE_SERVER_IP not found in .env file.")
        return

    # 2. Initialize the Remote Embedding Model
    # MXBAI-EMBED-LARGE is state-of-the-art for local RAG
    embeddings = OllamaEmbeddings(
        base_url=f"http://{inference_server_ip}:11434",
        model="mxbai-embed-large"
    )

    # 3. Process each PDF in the data folder
    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        add_start_index=True # Crucial for citation
    )

    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):
            logger.info(f"Processing {filename}...")
            file_path = os.path.join(data_folder, filename)
            
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            
            chunks = text_splitter.split_documents(docs)
            all_chunks.extend(chunks)
    
    logger.info(f"Total chunks created: {len(all_chunks)}")

    # 4. Create and Persist the Vector Database
    logger.info("Connecting to Inference Server for vectorization (this may take a moment)...")
    
    vector_db = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory=db_folder
    )
    
    logger.info(f"Successfully saved vector database to {db_folder}")

if __name__ == "__main__":
    ingest_docs()