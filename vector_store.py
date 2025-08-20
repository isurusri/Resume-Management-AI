import streamlit as st
from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import chromadb
from chromadb.config import Settings

import config

class VectorStore:
    def __init__(self, model_name: str = config.DEFAULT_MODEL):
        self.embeddings = OllamaEmbeddings(base_url=config.OLLAMA_BASE_URL, model=model_name)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=config.CHROMA_DB_DIR,
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )

        self.vector_store = None
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initialize or load existing vector store."""
        try:
            self.vector_store = Chroma(
                client=self.client,
                collection_name=config.COLLECTION_NAME,
                embedding_function=self.embeddings,
            )
        except Exception as e:
            st.error(f"Error initializing vector store: {e}")

    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to the vector store."""
        if not documents:
            return False

        try:
            self.vector_store.add_documents(documents)
            return True
        except Exception as e:
            st.error(f"Error adding documents: {e}")
            return False

    def get_retriever(self, k: int = 5):  # More context for resumes
        """Get retriever for RAG chain."""
        if not self.vector_store:
            return None
        return self.vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": k}
        )

    def clear_database(self):
        """Clear the vector database."""
        try:
            self.client.delete_collection(config.COLLECTION_NAME)
            self._initialize_vector_store()
            return True
        except Exception as e:
            st.error(f"Error clearing database: {e}")
            return False
