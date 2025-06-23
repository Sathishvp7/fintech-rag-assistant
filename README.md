# RAG System with Role-Based Access Control (RBAC)

This project implements a Retrieval-Augmented Generation (RAG) system with a Role-Based Access Control (RBAC) layer to demonstrate how to provide context-aware, permission-sensitive answers from a knowledge base.

The application is composed of three main parts:
1.  **Ingestion Script**: A script to process source documents and store them in a vector database with role-based metadata.
2.  **Backend API**: A FastAPI application that serves the RAG pipeline, filtering retrieved documents based on the user's role.
3.  **Frontend UI**: A Streamlit application that provides a user-friendly interface to interact with the RAG system.

## Features

-   **Role-Based Access Control**: Restricts access to information based on predefined user roles (e.g., C-Level, HR, Finance, Engineering, Marketing, Employee).
-   **Retrieval-Augmented Generation**: Uses a vector database (ChromaDB) and a Large Language Model (OpenAI's GPT) to answer questions based on a set of documents.
-   **FastAPI Backend**: A robust and fast API for serving the RAG pipeline.
-   **Streamlit Frontend**: An interactive web interface for users to ask questions and receive answers.
-   **Modular Design**: The project is structured into separate components for ingestion, backend, and frontend, making it easy to maintain and extend.

## Project Structure

```
.  
├── backend/  
│   ├── .env                # Environment variables for the backend (needs to be created)  
│   ├── main.py             # FastAPI application  
│   └── requirements.txt    # Python dependencies for the backend  
├── data/                   # Source documents for ingestion (needs to be created)  
│   ├── engineering/  
│   ├── finance/  
│   ├── marketing/  
│   ├── general_employee_handbook.md  
│   └── hr_data.csv  
├── frontend/  
│   ├── app.py              # Streamlit application  
│   └── requirements.txt    # Python dependencies for the frontend  
├── my_db5/                 # ChromaDB vector store (created by ingest.py)  
├── development_rag_notebook.ipynb # Script to ingest data into ChromaDB
├── evaluation_notebook_good.ipynb # Evaluating Model
└── README.md               # This file
```

## Prerequisites

-   Python 3.8+
-   An OpenAI API key

## Setup and Installation

1.  **Clone the repository** (if you haven't already).

2.  **Set up the Backend**:

    -   Navigate to the `backend` directory:
        ```bash
        cd backend
        ```
    -   Create a virtual environment:
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
        ```
    -   Install the required packages:
        ```bash
        pip install -r requirements.txt
        ```
    -   Create a `.env` file in the `backend` directory and add your OpenAI API key:
        ```
        OPENAI_API_KEY="your-openai-api-key"
        ```

3.  **Set up the Frontend**:

    -   Navigate to the `frontend` directory:
        ```bash
        cd ../frontend
        ```
    -   Create a virtual environment:
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
        ```
    -   Install the required packages:
        ```bash
        pip install -r requirements.txt
        ```

## Data Ingestion - development_rag_notebook.ipynb

Before running the application, you need to ingest the data into the vector store.

1.  **Create a `data` directory** in the root of the project.

2.  **Populate the `data` directory** with your source documents, following the structure mentioned in the "Project Structure" section.

3.  **Run the ingestion script** from the root directory:

    ```bash
    # Make sure you have the backend's virtual environment activated
    # or install the necessary packages in your global environment.
    # The ingest script requires packages from the backend's requirements.txt
    pip install -r backend/requirements.txt
    Run development_rag_notebook.ipynb Notebook
    ```

    This will create the `my_db5` directory containing the ChromaDB vector store.

## Running the Application

You need to run the backend and frontend servers in separate terminals.

1.  **Run the Backend API**:

    -   Navigate to the `backend` directory and activate its virtual environment.
    -   Run the FastAPI server:
        ```bash
        uvicorn main:app --reload --port 8000
        ```

2.  **Run the Frontend UI**:

    -   Navigate to the `frontend` directory and activate its virtual environment.
    -   Run the Streamlit app:
        ```bash
        streamlit run app.py
        ```

    The Streamlit application will open in your browser.

## How to Use

1.  Open the Streamlit application in your web browser.
2.  Select a user role from the dropdown menu in the sidebar.
3.  Type your question in the text input field.
4.  Click the "Get Answer" button.
5.  The system will display the answer and the sources used to generate it, respecting the access level of the selected role.

## Technologies Used

-   **Backend**: FastAPI, LangChain, ChromaDB, OpenAI
-   **Frontend**: Streamlit
-   **Language**: Python
