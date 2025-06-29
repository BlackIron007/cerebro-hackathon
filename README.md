#  CEREBRO: The Autonomous AI Analyst

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-blue?style=for-the-badge&logo=ibm)](https://www.ibm.com/watsonx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

CEREBRO is a groundbreaking autonomous AI agent that ingests, understands, creates, and self-heals code, acting as an expert technical partner for any developer tackling a complex codebase.

---

##  Demo Video & Live Application

*   **Watch my 3-minute demo video:** [https://drive.google.com/file/d/1jIiXXanPdzQJmgmZW_puYzJVydh5lKQB/view?usp=sharing]
*   **Interact with the live application:** [https://cerebro-hackathon-ktjhtmf7ak5ihnb9kbhu7m.streamlit.app/]

---

###  A Note on the Demo Video Submission

Due to a technical issue with my recording setup discovered only after the final submission, the voiceover track for my demo video was not included in the final render.

To provide the full context and intended narration for our demonstration, I have included the complete voiceover script below. I kindly request that you read along with the script while watching the video to fully experience the CEREBRO demonstration as intended. I appreciate your understanding.

---

### **Voiceover Script**

> **The Problem & The Introduction**
> 
> "The single greatest bottleneck in software development isn't writing new code. It's understanding what's already there. Developers spend up to seventy percent of their time navigating complex, undocumented codebases. This comprehension tax costs the industry billions in lost productivity. To solve this, we built CEREBRO: an autonomous AI analyst, powered by IBM Granite, designed to make any codebase instantly understandable."
> 
> ---
> 
> **The Demo Part 1: Trustworthy Analysis**
> 
> "First, let's see CEREBRO's analysis capability. It has already ingested and analyzed the entire Python 'requests' library. I'll ask it a specific, practical question about a core concept -  the Session object."
> 
> "As you can see, it instantly provides a correct summary. This is perfect for quick triage when a developer needs a fast definition without context-switching. This isn't generic knowledge; it's grounded, context-aware analysis."
> 
> ---
> 
> **The Demo Part 2: The "Wow Moment" - Creation & Self-Healing**
> 
> "But CEREBRO's true power is not just in analysis, but in its ability to create and autonomously debug new code. I'll now give it a task that's specifically designed to fail, to showcase its self-healing loop. I already have it on my clipboard to save time - Write a function named safe_divide that takes two numbers, a and b, and returns a / b."
> 
> "CEREBRO is now engaging its multi-step autonomous workflow. What you're seeing is the end of a complex process. In its first attempt, CEREBRO generated a simple but flawed function. Its own autonomous QA agent then wrote a unit test that correctly failed with a ZeroDivisionError. CEREBRO then analyzed that failure, and without any human intervention, rewrote the code to create this final, robust version that handles the edge case correctly. It then re-ran the tests and confirmed VALIDATION PASSED. CEREBRO has autonomously healed its own code!"
> 
> ---
> 
> **The Technical Core & Conclusion**
> 
> "This entire process was accomplished using a team of specialized IBM Granite models on watsonx.ai: a retrieval model to build the knowledge base, an instruction model for analysis and QA, and a dedicated code model for generation and debugging. CEREBRO represents a new paradigm for developer tools. By automating the cycles of understanding, creation, and debugging, it has the potential to fundamentally accelerate software innovation. Thank you."


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
