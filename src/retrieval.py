import os
import logging
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def get_retrieval_chain():
    # 1. Setup Inference Server for Embeddings
    inference_url = os.getenv("INFERENCE_SERVER_URL")
    embeddings = OllamaEmbeddings(
        base_url=inference_url,
        model="mxbai-embed-large"
    )

    # 2. Connect to the existing Vector DB
    vector_db = Chroma(
        persist_directory="./vector_db", 
        embedding_function=embeddings
    )

    # 3. Setup Watsonx.ai LLM
    # We use Granite-3.0-8b or Llama-3-70b depending on your project needs
    watsonx_llm = WatsonxLLM(
        model_id="ibm/granite-3-8b-instruct",
        url="https://us-south.ml.cloud.ibm.com",
        project_id=os.getenv("PROJECT_ID"),
        params={
            "decoding_method": "sample",
            "max_new_tokens": 512,
            "temperature": 0.2, # Low temperature for factual RAG
        }
    )

    # 4. Define a Professional RAG Prompt
    # This prevents the AI from "hallucinating" or using outside knowledge
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Keep the answer as concise as possible. Always cite the source document name.

    {context}

    Question: {question}
    Helpful Answer:"""

    RAG_PROMPT = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )

    # 5. Build the Chain
    chain = RetrievalQA.from_chain_type(
        llm=watsonx_llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": RAG_PROMPT},
        return_source_documents=True # Critical for the UI to show citations
    )
    
    return chain

if __name__ == "__main__":
    # Quick Test
    qa_chain = get_retrieval_chain()
    query = "What are the main requirements of this contract?"
    result = qa_chain.invoke({"query": query})
    
    print(f"\nAnswer: {result['result']}")
    print("\nSources:")
    for doc in result['source_documents']:
        print(f"- {doc.metadata['source']} (Page {doc.metadata.get('page', 'N/A')})")