# 📚 Local Document QA Assistant

A privacy-focused, AI-powered document question-answering system that runs entirely on your local machine. Built with Ollama, LangChain, ChromaDB, and Streamlit for secure, offline document analysis.

## ✨ Features

- 🔒 **100% Local Processing** - No data ever leaves your machine
- 📄 **Multiple Document Formats** - PDF, TXT, DOCX, MD support
- 🤖 **Open Source LLMs** - Powered by Ollama (Gemma, Llama3, etc.)
- 🔍 **Intelligent Search** - Vector similarity search with ChromaDB
- 💬 **Chat Interface** - Natural conversation with your documents
- 📊 **Source Attribution** - See exactly which documents answered your questions
- ⚡ **Resume Analysis Mode** - Specialized prompts for HR and recruiting
- 🚀 **Easy Setup** - One-command installation and deployment

## 🎯 Use Cases

### General Document QA
- Company handbook queries
- Technical documentation search
- Policy and procedure questions
- Research paper analysis
- Legal document review

### Resume Analysis (Specialized Mode)
- Technical skills assessment
- Experience evaluation
- Career progression analysis
- Candidate comparison
- Role-specific matching
- Red flag identification

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- 8GB+ RAM (16GB recommended for larger models)
- 10GB+ free disk space

### Option 1: Automated Setup (Recommended)

```bash
# Download and run setup script
curl -O https://raw.githubusercontent.com/your-repo/local-doc-qa/main/setup.sh
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

#### 1. Install Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows - Download from https://ollama.ai/download
```

#### 2. Clone and Setup Project
```bash
git clone https://github.com/your-repo/local-doc-qa.git
cd local-doc-qa
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. Start Ollama and Pull Models
```bash
# Start Ollama service
ollama serve

# Pull recommended models (choose one)
ollama pull gemma:2b      # Lightweight, fast
ollama pull gemma:7b      # Better quality, more RAM
ollama pull llama3:8b     # Best quality, most RAM
```

#### 4. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
local-doc-qa/
├── app.py                    # Main Streamlit application
├── resume_analyzer.py        # Specialized resume analysis app
├── document_processor.py     # Document loading and chunking
├── vector_store.py          # ChromaDB vector operations
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── setup.sh                 # Automated setup script
├── README.md               # This file
├── documents/              # Document upload directory
├── chroma_db/             # Vector database storage
└── examples/              # Sample documents and notebooks
```

## 🔧 Configuration

### Model Selection
Edit `config.py` to change the default model:
```python
DEFAULT_MODEL = "gemma:7b"  # or "llama3:8b", "gemma:2b"
```

### Performance Tuning
Adjust chunk sizes for your document types:
```python
CHUNK_SIZE = 1000      # Larger for technical docs
CHUNK_OVERLAP = 200    # Overlap for context preservation
```

### Advanced Settings
```python
# Vector search results
RETRIEVAL_K = 3        # Number of document chunks to retrieve

# LLM Parameters
TEMPERATURE = 0.1      # Lower = more focused, Higher = more creative
```

## 📖 Usage Guide

### Basic Document QA

1. **Upload Documents**: Use the sidebar file uploader
2. **Process**: Click "Process Documents" to add to vector database
3. **Ask Questions**: Type natural language questions about your documents
4. **View Sources**: Expand source sections to see supporting content

#### Example Questions:
```
- "What is the company's vacation policy?"
- "How do I set up the development environment?"
- "What are the safety requirements for this procedure?"
- "Summarize the key findings from this research paper"
```

### Resume Analysis Mode

#### Quick Analysis
Use the pre-built analysis buttons:
- **Summary**: Comprehensive candidate overview
- **Technical Skills**: Programming languages and technologies
- **Experience**: Career progression and achievements
- **Education**: Degrees, certifications, training
- **Leadership**: Management and team experience
- **Red Flags**: Potential concerns or gaps

#### Custom Analysis Questions
```
Technical Assessment:
- "What programming languages does this candidate know?"
- "List all cloud platforms and DevOps tools mentioned"
- "What machine learning or AI experience is highlighted?"

Experience Evaluation:
- "Summarize this candidate's career progression"
- "What are their most significant achievements?"
- "How many years of leadership experience do they have?"

Role Matching:
- "How well does this candidate match a Senior Python Developer role?"
- "What skills are missing for a DevOps Engineer position?"
- "Compare all candidates for a Data Scientist role"
```

## 🎨 Advanced Features

### Multiple Document Analysis
Load multiple documents for comparative analysis:
```
- "Compare the policies between Document A and Document B"
- "Which candidate has the most Python experience?"
- "What are the common themes across all research papers?"
```

### Custom Prompt Templates
Modify prompts for specific domains in `app.py`:
```python
# Legal document analysis
legal_prompt = """You are analyzing legal documents. Provide precise answers 
based only on the provided context. If uncertain, state your limitations..."""

# Technical documentation
tech_prompt = """You are a technical expert. Provide detailed answers with 
code examples when applicable..."""
```

### Batch Processing
Process entire directories of documents:
```python
# Add to document_processor.py
def process_directory(self, directory_path):
    file_paths = self.get_documents_from_directory(directory_path)
    return self.process_documents(file_paths)
```

## 🔧 Troubleshooting

### Common Issues

#### Ollama Connection Error
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

#### Model Not Found
```bash
# List available models
ollama list

# Pull missing model
ollama pull gemma:2b
```

#### Memory Issues
- Use smaller models (`gemma:2b` instead of `llama3:8b`)
- Reduce chunk size in config
- Process fewer documents at once
- Increase system RAM or swap

#### Document Processing Errors
- Check file permissions
- Ensure supported file formats (PDF, TXT, DOCX, MD)
- Verify file integrity
- Try processing files individually

#### ChromaDB Issues
```bash
# Clear corrupted database
rm -rf chroma_db/
# Restart application to recreate
```

### Performance Optimization

#### For Better Speed:
- Use `gemma:2b` model
- Reduce `CHUNK_SIZE` and `RETRIEVAL_K`
- Use SSD storage for ChromaDB
- Limit concurrent document processing

#### For Better Accuracy:
- Use `llama3:8b` or `gemma:7b` models
- Increase `RETRIEVAL_K` to 5-7
- Optimize chunk size for your document types
- Use more specific questions

## 🔒 Privacy & Security

### Data Protection
- **Local Processing**: All data stays on your machine
- **No Internet Required**: Works completely offline after setup
- **No Cloud APIs**: No data sent to external services
- **Encrypted Storage**: ChromaDB supports encryption at rest

### Best Practices
- Use dedicated environments for sensitive documents
- Regular database backups
- Access control for multi-user deployments
- Audit logging for compliance requirements

## 🛠️ Development

### Adding New Document Types
```python
# In document_processor.py
elif file_extension == '.csv':
    loader = CSVLoader(file_path)
elif file_extension == '.html':
    loader = UnstructuredHTMLLoader(file_path)
```

### Custom Embeddings
```python
# In vector_store.py
from sentence_transformers import SentenceTransformer

self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
```

### API Integration
```python
# Create FastAPI wrapper
from fastapi import FastAPI
app = FastAPI()

@app.post("/query")
async def query_documents(question: str):
    # Your QA logic here
    return {"answer": response, "sources": sources}
```

## 📊 System Requirements

### Minimum Requirements
- **CPU**: 4 cores, 2.0GHz
- **RAM**: 8GB (for gemma:2b)
- **Storage**: 10GB free space
- **OS**: Windows 10/11, macOS 10.15+, Linux

### Recommended Requirements
- **CPU**: 8 cores, 3.0GHz+
- **RAM**: 16GB+ (for larger models)
- **Storage**: 50GB+ SSD
- **GPU**: Optional, for faster processing

### Model Requirements
| Model | RAM Usage | Quality | Speed |
|-------|-----------|---------|-------|
| gemma:2b | ~4GB | Good | Fast |
| gemma:7b | ~8GB | Better | Medium |
| llama3:8b | ~12GB | Best | Slow |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/your-repo/local-doc-qa.git
cd local-doc-qa
python -m venv dev-env
source dev-env/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

### Running Tests
```bash
pytest tests/
streamlit run app.py --server.headless true --server.port 8502
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM serving
- [LangChain](https://langchain.com/) for RAG framework
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Streamlit](https://streamlit.io/) for the web interface

## 🆘 Support

- 📖 [Documentation](https://your-docs-site.com)
- 💬 [Discussions](https://github.com/your-repo/local-doc-qa/discussions)
- 🐛 [Issues](https://github.com/your-repo/local-doc-qa/issues)
- 📧 [Email Support](mailto:support@yourproject.com)

## 🗺️ Roadmap

### Upcoming Features
- [ ] Multi-language document support
- [ ] Advanced analytics dashboard
- [ ] Docker containerization
- [ ] REST API
- [ ] Collaborative features
- [ ] Integration with popular tools (Slack, Teams)
- [ ] Advanced security features
- [ ] Cloud deployment guides

### Version History
- **v1.0.0** - Initial release with basic QA functionality
- **v1.1.0** - Added resume analysis mode
- **v1.2.0** - Performance improvements and bug fixes
- **v2.0.0** - (Planned) Advanced analytics and API

---

**Made with ❤️ for privacy-focused document analysis**