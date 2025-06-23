import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

# Load environment variables
load_dotenv()

# --- Configuration ---
DB_DIR = r"C:\Users\sathish.anantharaj\Documents\Projects\code_basics_projects\DS-RPC-01\code\my_db5"
COLLECTION_NAME = "rbac_rag_store"

# --- Pydantic Models for Request/Response ---
class QueryRequest(BaseModel):
    question: str
    user_role: str

class QueryResponse(BaseModel):
    question: str
    user_role: str
    answer: str
    sources: str

# --- FastAPI App Initialization ---
app = FastAPI()

# --- Global Variables (loaded on startup) ---
vector_store = None
rag_chain = None

@app.on_event("startup")
def startup_event():
    global vector_store, rag_chain

    # Check if the database exists
    if not os.path.exists(DB_DIR):
        raise RuntimeError(
            f"Vector store not found at {DB_DIR}. "
            f"Please run the ingest.py script first."
        )

    # Load the vector store
    print("Loading vector store...")
    openai_embed_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma(
        persist_directory=DB_DIR,
        embedding_function=openai_embed_model,
        collection_name=COLLECTION_NAME
    )
    print("Vector store loaded successfully.")

    # Define the RAG prompt template
    rag_prompt_template = ChatPromptTemplate.from_template(
        """You are an expert question-answering assistant.
        Answer the question based only on the provided context.
        If the answer is not in the context, say 'I don't know'.

        Context:
        {context}

        Question:
        {question}
        """
    )

    # Initialize the language model
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    # Define a function to format docs
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Define a function to get a role-based retriever
    def get_rbac_retriever(user_role: str):
        if user_role.lower() == "c-level":
            # C-Level gets access to all documents, so no filter is applied.
            return vector_store.as_retriever(search_kwargs={"k": 3})
        else:
            # For other roles, filter by their specific access level.
            return vector_store.as_retriever(
                search_kwargs={"k": 3, "filter": {"access_level": user_role}}
            )

    # Build the RAG chain
    rag_chain = (
        {
            "context": lambda x: get_rbac_retriever(x["user_role"]).invoke(x["question"]),
            "question": itemgetter("question"),
            "user_role": itemgetter("user_role")
        }
        | RunnablePassthrough.assign(
            answer=(
                {
                    "context": lambda x: format_docs(x["context"]),
                    "question": itemgetter("question")
                }
                | rag_prompt_template
                | llm
                | StrOutputParser()
            )
        )
    )
    print("RAG chain created successfully.")


@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    if not rag_chain:
        raise HTTPException(status_code=503, detail="RAG chain is not initialized.")

    try:
        # Invoke the RAG chain
        result = rag_chain.invoke({"question": request.question, "user_role": request.user_role})

        print("CONTEXT .......................")
        for i, doc in enumerate(result['context']):
            print(f"--- Document {i+1} ---")
            print("Content:", doc.page_content[:200])
            print("Metadata:", doc.metadata)
            print()

        print('#' * 40)

        # Format source info
        sources = "\n".join([
            f"- File: {doc.metadata.get('file_name', 'N/A')}, "
            f"Page: {doc.metadata.get('page_no', 'N/A')}, "
            for doc in result['context']
        ])

        return QueryResponse(
            question=result["question"],
            user_role=request.user_role,
            answer=result["answer"],
            sources=sources
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "RBAC RAG API is running. Use the /query endpoint to ask questions."}
