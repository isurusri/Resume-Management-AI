import streamlit as st
import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

import config

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def load_document(self, file_path: str) -> List[Document]:
        """Load a single document based on its extension."""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension in ['.txt', '.md']:
                loader = TextLoader(file_path, encoding='utf-8')
            elif file_extension == '.docx':
                loader = Docx2txtLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            documents = loader.load()
            # Add filename to metadata
            for doc in documents:
                doc.metadata['filename'] = os.path.basename(file_path)
            return documents
        
        except Exception as e:
            st.error(f"Error loading {file_path}: {str(e)}")
            return []
    
    def process_documents(self, file_paths: List[str]) -> List[Document]:
        """Process multiple documents and return chunks."""
        all_documents = []
        
        for file_path in file_paths:
            docs = self.load_document(file_path)
            all_documents.extend(docs)
        
        if not all_documents:
            return []
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(all_documents)
        
        return chunks
