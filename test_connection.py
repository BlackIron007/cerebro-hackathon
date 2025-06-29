import os
from dotenv import load_dotenv
from langchain_community.llms import WatsonxLLM

load_dotenv()
api_key = os.getenv("WATSONX_APIKEY")
project_id = os.getenv("WATSONX_PROJECT_ID")

if not api_key or not project_id:
    print("Error: Make sure you have created a .env file with your IBM_API_KEY and IBM_PROJECT_ID")
    exit()

print("Credentials loaded successfully.")

model_id = "ibm/granite-13b-instruct-v2" 

params = {
    "decoding_method": "greedy",
    "max_new_tokens": 200,
    "min_new_tokens": 1,
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 1,
}

try:
    print(f"Connecting to watsonx.ai with Project ID: {project_id}...")
    watsonx_llm = WatsonxLLM(
        model_id=model_id,
        url="https://us-south.ml.cloud.ibm.com",
        project_id=project_id,
        params=params,
    )
    print("Connection object created.")

    prompt = "Hello, Granite! In one short sentence, what is the key to a successful hackathon?"
    print(f"\nSending prompt: '{prompt}'")
    
    response = watsonx_llm.invoke(prompt)

    print("\n--- Response from Granite ---")
    print(response)
    print("---------------------------\n")
    print("Connection successful!")

except Exception as e:
    print(f"An error occurred: {e}")