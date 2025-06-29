import os
import shutil
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_ibm import WatsonxEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.tools import tool

PERSIST_DIRECTORY = "db"

vector_store = None

@tool("Codebase Search Tool")
def codebase_search_tool(query: str) -> dict:
    """
    Searches a vector database of a codebase to find relevant code snippets
    and returns them as a dictionary containing the context and a list of sources.
    """
    global vector_store
    if vector_store is None:
        return {"context": "Error: The vector store has not been loaded.", "sources": []}

    print(f"\n---[Codebase Search Tool]: Received query: '{query}'---")
    
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8, "fetch_k": 25}
    )
    relevant_docs = retriever.invoke(query)
    
    if not relevant_docs:
        return {"context": "No relevant documents found in the codebase for this query.", "sources": []}

    context = "\n\n".join([f"Source: {doc.metadata['source']}\n---\n{doc.page_content}" for doc in relevant_docs])
    
    sources = [
        {"source": doc.metadata.get("source", "Unknown"), "content": doc.page_content}
        for doc in relevant_docs
    ]
    
    return {"context": context, "sources": sources}

def initialize_and_build_vector_store(documents: list[tuple[str, str]], repo_name: str):
    """
    Creates and saves a new vector store for a given repository.
    This function will overwrite any existing store for the same repo name.
    """
    global vector_store
    print(f"Building a new vector store for '{repo_name}'...")
    
    repo_db_path = os.path.join(PERSIST_DIRECTORY, repo_name)

    if os.path.exists(repo_db_path):
        print(f"Removing old database at {repo_db_path}")
        shutil.rmtree(repo_db_path)

    langchain_docs = []
    for path, content in documents:
        doc = Document(page_content=content, metadata={"source": path})
        langchain_docs.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(langchain_docs)
    
    if not chunks:
        raise ValueError("No chunks were created. Cannot build vector store.")

    load_dotenv()
    project_id = os.getenv("WATSONX_PROJECT_ID")
    embeddings = WatsonxEmbeddings(
        model_id="ibm/slate-125m-english-rtrvr",
        url="https://us-south.ml.cloud.ibm.com",
        project_id=project_id,
    )

    print("Generating embeddings and creating persistent ChromaDB vector store...")
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings,
        persist_directory=repo_db_path
    )
    print(f"Vector store created and saved to '{repo_db_path}'.")
    return True

def load_vector_store(repo_name: str) -> bool:
    """
    Loads an existing vector store from disk.
    Returns True if successful, False otherwise.
    """
    global vector_store
    repo_db_path = os.path.join(PERSIST_DIRECTORY, repo_name)
    
    if not os.path.exists(repo_db_path):
        return False

    print(f"Loading existing vector store from '{repo_db_path}'...")
    
    load_dotenv()
    project_id = os.getenv("WATSONX_PROJECT_ID")
    embeddings = WatsonxEmbeddings(
        model_id="ibm/slate-125m-english-rtrvr",
        url="https://us-south.ml.cloud.ibm.com",
        project_id=project_id,
    )
    
    vector_store = Chroma(
        persist_directory=repo_db_path,
        embedding_function=embeddings
    )
    print("Vector store loaded successfully.")
    return True