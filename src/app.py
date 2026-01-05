import os
import gradio as gr
from retrieval import get_retrieval_chain

# Initialize the RAG chain
print("--- Initializing RAG System ---")
qa_chain = get_retrieval_chain()

def respond(message, history):
    """
    Main function to handle user queries.
    Returns the answer and formats the sources for the UI.
    """
    try:
        # Run the retrieval chain
        response = qa_chain.invoke({"query": message})
        answer = response["result"]
        sources = response["source_documents"]

        # Format sources for a professional look
        source_list = "\n\n**Sources:**\n"
        unique_sources = set()
        for doc in sources:
            name = os.path.basename(doc.metadata.get("source", "Unknown"))
            page = doc.metadata.get("page", "N/A")
            unique_sources.add(f"- {name} (Page {page})")
        
        full_response = answer + source_list + "\n".join(unique_sources)
        return full_response

    except Exception as e:
        return f"Error connecting to Inference Server or Watsonx: {str(e)}"

# Define a professional, dark-themed UI
demo = gr.ChatInterface(
    fn=respond,
    title="Hybrid-RAG Agent (Doc-Bot)",
    description="Analyze sensitive PDFs using a local Inference Server and IBM Watsonx.ai.",
    examples=["What are the key terms in this document?", "Summarize the liability clauses."],
    theme=gr.themes.Soft(),
    type="messages"
)

if __name__ == "__main__":
    # Server configuration for Docker
    # We use 0.0.0.0 so the port can be forwarded out of the container
    demo.launch(server_name="0.0.0.0", server_port=7860)