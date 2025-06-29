import os
import re
import shutil
import streamlit as st
from dotenv import load_dotenv

from langchain_ibm import WatsonxLLM
from langchain_experimental.tools import PythonREPLTool

from codebase_loader import load_repo
from rag_engine import initialize_and_build_vector_store, load_vector_store, codebase_search_tool

st.set_page_config(
    page_title="CEREBRO Code Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    st.markdown("""
        <style>
            /* Import a modern font */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            html, body, [class*="st-"] {
                font-family: 'Inter', sans-serif;
            }
            
            /* Hide Streamlit's default header and hamburger menu */
            header {visibility: hidden;}
            .main {
                background-color: #0E1117; /* A deep, dark background */
            }

            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background-color: #1E1E2F;
                border-right: 1px solid #2E2E48;
            }
            [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
                color: #FFFFFF;
            }
            [data-testid="stSidebar"] .stButton>button {
                font-weight: 600;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                border: 1px solid #4A4A5E;
                background-color: transparent;
                color: #D0D0D0;
                transition: all .2s ease-in-out;
                width: 100%;
            }
            [data-testid="stSidebar"] .stButton>button:hover {
                background-color: #4A4A5E;
                color: #FFFFFF;
                border-color: #f63366;
            }
            [data-testid="stSidebar"] .stButton>button[kind="primary"] {
                 background-image: linear-gradient(to right, #f63366 0%, #E64573 100%);
                 border: none;
                 color: white;
            }

            /* Main chat message styling */
            [data-testid="chat-container"] [data-testid="stChatMessage"] {
                background-color: #1E1E2F;
                border: 1px solid #2E2E48;
                border-radius: 12px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

load_dotenv()
load_css()
project_id = os.getenv("WATSONX_PROJECT_ID")
if not project_id or not os.getenv("WATSONX_APIKEY"):
    st.error("FATAL: Watsonx credentials not found.")
    st.stop()

def get_repo_name(url: str) -> str:
    match = re.search(r'github\.com/([^/]+)/([^/]+)', url)
    if match: return f"{match.group(1)}_{match.group(2)}"
    return "default_repo"

def extract_python_code(text: str) -> str:
    pattern = r"```(?:python)?(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match: return match.group(1).strip()
    return text.strip()

if "repo_loaded" not in st.session_state: st.session_state.repo_loaded = False
if "current_repo" not in st.session_state: st.session_state.current_repo = ""
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.title("CEREBRO")
    st.caption("v1.0 - The Autonomous Analyst")
    st.header("Control Panel")
    
    st.subheader("1. Load Codebase")
    repo_url = st.text_input("Public GitHub Repo URL", value="https://github.com/psf/requests", label_visibility="collapsed")
    
    if st.button("Analyze Repository", type="primary", use_container_width=True):
         if repo_url:
            with st.spinner("CEREBRO is assimilating the codebase..."):
                repo_name = get_repo_name(repo_url)
                st.session_state.current_repo = repo_name
                st.session_state.messages = []
                if load_vector_store(repo_name):
                    st.session_state.repo_loaded = True
                else:
                    try:
                        code_files = load_repo(repo_url)
                        if code_files:
                            initialize_and_build_vector_store(code_files, repo_name)
                            st.session_state.repo_loaded = True
                    except Exception as e:
                        st.error(f"Analysis Failed: {e}")
                        st.session_state.repo_loaded = False
            if st.session_state.repo_loaded:
                st.success(f"Knowledge base for '{repo_name}' loaded!")
    
    st.divider()
    st.subheader("Developer Tools")
    if st.button("Clear All Knowledge Bases", use_container_width=True):
        db_path = "db"
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
            st.success("All cached knowledge bases cleared.")
            st.session_state.repo_loaded = False
            st.session_state.current_repo = ""
            st.session_state.messages = []
        else:
            st.info("No knowledge bases to clear.")

st.title("Command Center")
st.text(f"Mission Target: {st.session_state.current_repo}" if st.session_state.current_repo else "No Mission Target")
st.divider()

if not st.session_state.repo_loaded:
    st.info("Awaiting instructions. Please analyze a repository from the Control Panel.")
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Define a task for CEREBRO..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Engaging AI Analyst Team..."):
                
                intent_llm = WatsonxLLM(model_id="ibm/granite-13b-instruct-v2",url="https://us-south.ml.cloud.ibm.com",project_id=project_id,params={"max_new_tokens": 20, "temperature": 0.0})
                intent_prompt = f"""Classify the user's intent: CREATION, ANALYSIS, or AMBIGUOUS.
- "write a function to sort a list" -> CREATION
- "how does the auth system work?" -> ANALYSIS
- "what is the Session object" -> ANALYSIS
- "hello" -> AMBIGUOUS
User Prompt: "{prompt}"
Classification:"""
                intent = intent_llm.invoke(intent_prompt).strip().upper()
                
                response_content = ""

                if "CREATION" in intent:
                    max_retries = 2
                    generated_code_output, validation_result = "", ""
                    code_llm = WatsonxLLM(model_id="ibm/granite-8b-code-instruct", url="https://us-south.ml.cloud.ibm.com", project_id=project_id, params={"max_new_tokens": 1000})
                    qa_llm = WatsonxLLM(model_id="ibm/granite-13b-instruct-v2", url="https://us-south.ml.cloud.ibm.com", project_id=project_id, params={"max_new_tokens": 1000})
                    python_repl = PythonREPLTool()
                    research_context = codebase_search_tool.run(prompt)["context"]

                    for i in range(max_retries):
                        if i == 0:
                            coder_prompt = f"Based on the context and user request, write a single, complete Python function. The final output must be ONLY the code block.\n\nCONTEXT:\n{research_context}\n\nUSER's REQUEST: {prompt}\n\nCODE:"
                        else:
                            coder_prompt = f"The previous code you wrote failed the validation test. Please analyze the error and write a new, corrected version of the code. The output must be ONLY the corrected code block.\n\nORIGINAL REQUEST: {prompt}\nBROKEN CODE:\n{generated_code_output}\nVALIDATION ERROR:\n{validation_result}\n\nCORRECTED CODE:"
                        generated_code_output = code_llm.invoke(coder_prompt)
                        
                        test_gen_prompt = f"""You are a QA Engineer. Write a test script for the given function. Include a test for a standard valid input and an edge case if applicable (like division by zero). Conclude by printing 'All tests passed.' if all checks are successful. The output must be ONLY the Python code block.
GENERATED FUNCTION: {generated_code_output}
TEST SCRIPT:"""
                        test_code_output = qa_llm.invoke(test_gen_prompt)
                        
                        clean_generated_code = extract_python_code(generated_code_output)
                        clean_test_code = extract_python_code(test_code_output)
                        full_test_script = clean_generated_code + "\n" + clean_test_code
                        
                        try:
                            execution_result = python_repl.run(full_test_script)
                            if "All tests passed." in execution_result or not execution_result.strip():
                                validation_result = "VALIDATION PASSED"
                                break
                            else:
                                validation_result = f"VALIDATION FAILED: {execution_result}"
                        except Exception as e:
                             validation_result = f"VALIDATION FAILED: {e}"
                    
                    final_code = extract_python_code(generated_code_output)
                    response_content = f"### Creation Task Debrief\n**Validation:** {validation_result}\n```python\n{final_code}\n```"
                    st.markdown(response_content)

                elif "ANALYSIS" in intent:
            
                    retrieval_result = codebase_search_tool.run(prompt)
                    context, sources = retrieval_result["context"], retrieval_result["sources"]
                    
                    if not sources:
                        response_content = "Could not find relevant context in the codebase."
                        st.warning(response_content)
                    else:
                        explainer_llm = WatsonxLLM(model_id="ibm/granite-13b-instruct-v2", url="https://us-south.ml.cloud.ibm.com", project_id=project_id, params={"max_new_tokens": 2048, "temperature": 0.05})
                        
                        explainer_prompt = f"""You are a hyper-literal AI assistant. Your only job is to answer the user's question by performing these two steps **in order**:
1.  **SUMMARIZE**: Read the provided CONTEXT and write a detailed explanation that answers the USER'S QUESTION.
2.  **QUOTE**: Find the single best code block from the CONTEXT that serves as a direct example and quote it exactly.

Your entire response MUST be structured using these exact markdown headings:
### Summary
### Code Example from Repository

CONTEXT:
---
{context}
---

USER'S QUESTION: {prompt}

RESPONSE:
"""
                        answer = explainer_llm.invoke(explainer_prompt)
                        st.markdown(answer)
                        response_content = answer

                        with st.expander("View Raw Context Used"):
                            for i, source_doc in enumerate(sources):
                                st.code(source_doc["content"], language="python")
                                st.caption(f"Source: {source_doc['source']}")
                
                else: 
                    response_content = "Request is ambiguous. Please clarify if you want me to **write code** or **explain something**."
                    st.info(response_content)
                
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            st.rerun()