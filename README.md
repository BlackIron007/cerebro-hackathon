# 🧠 CEREBRO: The Autonomous AI Analyst

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-blue?style=for-the-badge&logo=ibm)](https://www.ibm.com/watsonx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

CEREBRO is a groundbreaking autonomous AI agent that ingests, understands, creates, and self-heals code, acting as an expert technical partner for any developer tackling a complex codebase.

---

##  Demo Video & Live Application

*   **Watch my 3-minute demo video:** [Your Demo Video Link Here]
*   **Interact with the live application:** [https://cerebro-hackathon-ktjhtmf7ak5ihnb9kbhu7m.streamlit.app/]

## The Problem: The Codebase Comprehension Bottleneck

In modern software development, developers spend up to 70% of their time navigating vast, complex, and often poorly documented codebases. This "comprehension tax" slows down innovation, makes onboarding new engineers difficult, and forces senior developers to spend more time explaining old code than writing new code. Existing tools can search for keywords, but they cannot provide a true, holistic understanding of a project's architecture and logic.

## Our Solution: An Autonomous Analyst

CEREBRO is designed to eliminate this bottleneck. It ingests an entire public GitHub repository and becomes a trusted, interactive expert on that specific project.

It features a unique, dual-workflow architecture powered by a team of specialized IBM Granite models:

1.  **Intent-Aware Analysis:** CEREBRO first classifies a user's natural language request as either an `ANALYSIS` or `CREATION` task.
2.  **Grounded Analysis Workflow:** For analysis, it uses a Retrieval-Augmented Generation (RAG) pipeline to provide detailed explanations and code examples that are **provably grounded in the repository's source code**, complete with source citations.
3.  **Self-Healing Creation Workflow:** For creation, CEREBRO autonomously writes new code, generates unit tests for it, executes those tests, and—if they fail—analyzes the error to debug and rewrite its own code until validation is passed.

This moves beyond a simple chatbot to an active, autonomous development partner that can reason, create, and self-correct.

##  Tech Stack

| Component            | Technology                                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| **UI Framework**     | Streamlit                                                                                                   |
| **AI Orchestration** | LangChain                                                                                                   |
| **AI Models**        | IBM Granite (`instruct-v2`, `code-instruct`, `slate-rtrvr`) on **watsonx.ai**                                 |
| **Vector Database**  | ChromaDB (for persistent knowledge base)                                                                    |
| **Code Execution**   | PythonREPLTool (sandboxed environment)                                                                      |

##  Setup and Local Installation

To run CEREBRO on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/cerebro-hackathon-submission.git
    cd cerebro-hackathon-submission
    ```

2.  **Set up a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create your secrets file:**
    *   Create a file named `.env` in the root of the project.
    *   Add your IBM Watsonx credentials to this file:
        ```
        WATSONX_APIKEY="your_ibm_cloud_api_key"
        WATSONX_PROJECT_ID="your_watsonx.ai_project_id"
        ```

5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

##  License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
