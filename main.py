from codebase_loader import load_repo
from rag_engine import RAG_Engine

TEST_REPO_URL = "https://github.com/psf/requests"
TEST_QUESTION = "How do you make a POST request using this library?"

if __name__ == "__main__":
    print("--- CEREBRO Full Pipeline Test ---")

    code_files = load_repo(TEST_REPO_URL)
    
    if not code_files:
        print("\n--- Test Failed: Could not load repository. ---")
    else:
        try:
            rag_system = RAG_Engine()
            rag_system.create_vector_store(code_files)
            
            answer = rag_system.answer_question(TEST_QUESTION)
            
            print("\n" + "="*50)
            print("          CEREBRO RESPONSE")
            print("="*50)
            print(f"Question: {TEST_QUESTION}\n")
            print(f"Answer: {answer}")
            print("="*50)

        except Exception as e:
            print(f"\nAn error occurred during the RAG process: {e}")
