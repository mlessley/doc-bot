import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM

load_dotenv()

def verify_handshake():
    try:
        llm = WatsonxLLM(
            model_id="ibm/granite-4-h-small",
            url="https://us-south.ml.cloud.ibm.com",
            project_id=os.getenv("PROJECT_ID")
        )
        print(f"IBM Watsonx Response: {llm.invoke('State your status.')}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    verify_handshake()