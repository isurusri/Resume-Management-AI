import streamlit as st
import os
import tempfile
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from document_processor import DocumentProcessor
from vector_store import VectorStore

import config

class ResumeAnalyzer:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        
        # Initialize session state
        if 'vector_store' not in st.session_state:
            st.session_state.vector_store = VectorStore()
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'resumes_processed' not in st.session_state:
            st.session_state.resumes_processed = []
        if 'current_prompt_type' not in st.session_state:
            st.session_state.current_prompt_type = "general"
        
        self.vector_store = st.session_state.vector_store
        
        # Initialize LLM
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.DEFAULT_MODEL,
            temperature=0.1
        )
    
    def get_prompt_template(self, prompt_type: str):
        """Get prompt template based on analysis type."""
        template = config.RESUME_PROMPTS.get(prompt_type, config.RESUME_PROMPTS["general"])
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def setup_qa_chain(self, prompt_type: str = "general"):
        """Setup the QA chain with retriever."""
        retriever = self.vector_store.get_retriever(k=5)
        if not retriever:
            return None
        
        prompt_template = self.get_prompt_template(prompt_type)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt_template},
            return_source_documents=True
        )
        
        return qa_chain
    
    def process_uploaded_files(self, uploaded_files):
        """Process uploaded files and add to vector store."""
        if not uploaded_files:
            return False
        
        temp_files = []
        processed_names = []
        
        try:
            # Save uploaded files to temporary directory
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    temp_files.append(tmp_file.name)
                    processed_names.append(uploaded_file.name)
            
            # Process documents
            documents = self.document_processor.process_documents(temp_files)
            if documents:
                success = self.vector_store.add_documents(documents)
                if success:
                    st.session_state.resumes_processed.extend(processed_names)
                return success
            return False
        
        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass
    
    def run(self):
        st.title("📄 Resume Analysis Assistant")
        st.markdown("**AI-powered resume analysis with local processing and privacy**")
        
        # Check Ollama connection
        try:
            self.llm.invoke("test")
            connection_status = "🟢 Connected"
        except Exception as e:
            connection_status = "🔴 Disconnected"
            st.error(f"Cannot connect to Ollama: {str(e)}")
            st.info("Make sure Ollama is running: `ollama serve` and model is available: `ollama pull gemma:2b`")
        
        # Sidebar for resume management
        with st.sidebar:
            st.header("📁 Resume Management")
            st.write(f"Status: {connection_status}")
            st.write(f"Model: {config.DEFAULT_MODEL}")
            st.write(f"Resumes loaded: {len(st.session_state.resumes_processed)}")
            
            if st.session_state.resumes_processed:
                with st.expander("📋 Loaded Resumes"):
                    for resume in st.session_state.resumes_processed:
                        st.write(f"• {resume}")
            
            st.divider()
            
            # File upload
            uploaded_files = st.file_uploader(
                "Upload Resume Files",
                type=['pdf', 'txt', 'docx'],
                accept_multiple_files=True,
                help="Upload PDF, TXT, or DOCX resume files"
            )
            
            if uploaded_files:
                if st.button("📤 Process Resumes", type="primary"):
                    with st.spinner("Processing resumes..."):
                        if self.process_uploaded_files(uploaded_files):
                            st.success(f"✅ Processed {len(uploaded_files)} resumes!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to process resumes")
            
            st.divider()
            
            # Analysis type selection
            st.header("🔍 Analysis Focus")
            prompt_type = st.selectbox(
                "Choose Analysis Type",
                options=["general", "technical", "experience", "match"],
                format_func=lambda x: {
                    "general": "🔍 General Analysis",
                    "technical": "💻 Technical Skills",
                    "experience": "💼 Work Experience", 
                    "match": "🎯 Role Matching"
                }[x],
                help="Select the type of analysis to perform"
            )
            st.session_state.current_prompt_type = prompt_type
            
            st.divider()
            
            # Quick analysis buttons
            st.header("⚡ Quick Analysis")
            for question_type, question in config.QUICK_QUESTIONS.items():
                if st.button(f"📊 {question_type}", key=f"quick_{question_type}"):
                    if st.session_state.resumes_processed:
                        st.session_state.messages.append({"role": "user", "content": question})
                        # Trigger analysis
                        st.session_state.pending_question = question
                        st.rerun()
                    else:
                        st.warning("Please upload resumes first!")
            
            st.divider()
            
            # Database management
            st.header("🗄️ Database")
            if st.button("🗑️ Clear All", type="secondary"):
                if self.vector_store.clear_database():
                    st.session_state.resumes_processed = []
                    st.session_state.messages = []
                    st.success("✅ Database cleared!")
                    st.rerun()
        
        # Main interface
        if not st.session_state.resumes_processed:
            st.info("👆 Please upload resume files to start your analysis!")
            
            # Show sample questions
            st.subheader("💡 Example Analysis Questions")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Technical Analysis:**
                - What programming languages does this candidate know?
                - List their technical certifications
                - What frameworks have they used?
                - Analyze their technical project experience
                """)
                
            with col2:
                st.markdown("""
                **Experience Analysis:**
                - Summarize their career progression
                - What leadership experience do they have?
                - Compare multiple candidates
                - Identify potential red flags
                """)
        
        else:
            st.header("💬 Resume Analysis Chat")
            
            # Display current analysis mode
            mode_display = {
                "general": "🔍 General Analysis Mode",
                "technical": "💻 Technical Skills Mode",
                "experience": "💼 Experience Analysis Mode",
                "match": "🎯 Role Matching Mode"
            }
            st.info(f"Current mode: {mode_display[st.session_state.current_prompt_type]}")
            
            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if "sources" in message and message["sources"]:
                        with st.expander("📄 Resume Sources"):
                            for i, source in enumerate(message["sources"]):
                                filename = source.metadata.get('filename', 'Unknown')
                                st.markdown(f"**📄 {filename}**")
                                st.markdown(f"```\n{source.page_content[:400]}...\n```")
            
            # Handle pending questions from quick analysis
            if hasattr(st.session_state, 'pending_question'):
                question = st.session_state.pending_question
                delattr(st.session_state, 'pending_question')
                
                with st.chat_message("assistant"):
                    try:
                        qa_chain = self.setup_qa_chain(st.session_state.current_prompt_type)
                        if qa_chain:
                            with st.spinner("🤔 Analyzing resumes..."):
                                result = qa_chain({"query": question})
                            
                            response = result["result"]
                            sources = result.get("source_documents", [])
                            
                            st.markdown(response)
                            
                            if sources:
                                with st.expander("📄 Resume Sources"):
                                    for i, source in enumerate(sources):
                                        filename = source.metadata.get('filename', 'Unknown')
                                        st.markdown(f"**📄 {filename}**")
                                        st.markdown(f"```\n{source.page_content[:400]}...\n```")
                            
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": response,
                                "sources": sources
                            })
                        else:
                            st.error("Unable to setup analysis chain.")
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg
                        })
            
            # Chat input
            if prompt := st.chat_input("Ask about the resumes..."):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Generate response
                with st.chat_message("assistant"):
                    try:
                        qa_chain = self.setup_qa_chain(st.session_state.current_prompt_type)
                        if not qa_chain:
                            st.error("Unable to setup analysis chain. Please check your resumes.")
                            return
                        
                        with st.spinner("🤔 Analyzing resumes..."):
                            result = qa_chain({"query": prompt})
                        
                        response = result["result"]
                        sources = result.get("source_documents", [])
                        
                        st.markdown(response)
                        
                        if sources:
                            with st.expander("📄 Resume Sources"):
                                for i, source in enumerate(sources):
                                    filename = source.metadata.get('filename', 'Unknown')
                                    st.markdown(f"**📄 {filename}**")
                                    st.markdown(f"```\n{source.page_content[:400]}...\n```")
                        
                        # Add assistant message
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response,
                            "sources": sources
                        })
                    
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg
                        })

def main():
    st.set_page_config(
        page_title="Resume Analysis Assistant",
        page_icon="📄",
        layout="wide"
    )
    
    # Check if Ollama is running
    try:
        test_llm = OllamaLLM(base_url=config.OLLAMA_BASE_URL, model=config.DEFAULT_MODEL)
        test_llm.invoke("test")
    except Exception:
        st.error("❌ Ollama is not running or model not found!")
        st.markdown("""
        **Please ensure:**
        1. Ollama is installed and running: `ollama serve`
        2. The model is pulled: `ollama pull gemma:2b`
        3. The model is available: `ollama list`
        """)
        st.stop()    
    # Run the app
    app = ResumeAnalyzer()
    app.run()

if __name__ == "__main__":
    main()