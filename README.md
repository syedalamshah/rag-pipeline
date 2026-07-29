[![Python CI](https://github.com/syedalamshah/rag-pipeline/actions/workflows/python-ci.yml/badge.svg)](https://github.com/syedalamshah/rag-pipeline/actions)

# RAG Pipeline

A beginner-friendly Python project that demonstrates Retrieval-Augmented Generation (RAG) using Google Gemini, LangChain, ChromaDB, and PyPDF. This pipeline loads a PDF, creates embeddings, stores them in a vector database, and uses an LLM to generate context-aware responses.

## What is RAG?

**RAG (Retrieval-Augmented Generation)** augments a language model with retrieved documents or knowledge at inference time. Instead of relying solely on the model's training data, RAG retrieves relevant context from a knowledge base and includes it in the prompt, enabling the model to provide accurate, grounded, and up-to-date answers.

### What This Project Does

1. **Load** — Extracts text from PDF documents using PyPDF
2. **Chunk** — Splits documents into overlapping chunks for better context preservation
3. **Embed** — Generates vector embeddings using Google's `gemini-embedding-001` model
4. **Index** — Stores embeddings in ChromaDB for fast similarity search
5. **Retrieve** — Fetches the most relevant chunks for a user query
6. **Generate** — Sends retrieved chunks + query to Google Gemini (`gemini-2.5-flash`) for intelligent response generation

## Tech Stack

| Component | Tool/Version |
|-----------|-------------|
| Language | Python 3.13 |
| LLM | Google Gemini (`gemini-2.5-flash`) |
| Embeddings | Google Generative AI (`gemini-embedding-001`) |
| Framework | LangChain |
| Vector Store | ChromaDB |
| PDF Parsing | PyPDF |

## Prerequisites

- **Git** — For cloning the repository
- **Python 3.13** — Download from [python.org](https://www.python.org/downloads/)
- **Google Cloud API Key** — With access to Generative AI (Gemini). Get one at [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Command Line / PowerShell** — Basic familiarity with terminal commands
- **Internet Connection** — To call Google APIs

## Installation

### 1. Clone the Repository

```powershell
git clone https://github.com/syedalamshah/rag-pipeline.git
cd rag-pipeline
```

### 2. Create and Activate Virtual Environment

```powershell
python -m venv venv
& "venv\Scripts\Activate.ps1"
```

### 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:

```powershell
copy .env.example .env
```

Edit `.env` and add your Google API key:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

**Do not share or commit your `.env` file.** It is already listed in `.gitignore`.

## How to Run

### Load and Preview the PDF

```powershell
python load_pdf.py
```

Output: Displays total pages and a preview of the first page's content.

### Split PDF into Chunks

```powershell
python chunk_pdf.py
```

Output: Shows total pages, total chunks created, and a preview of the first chunk.

### Run the RAG Pipeline

```powershell
python rag.py
```

This orchestrates the full pipeline: retrieves relevant chunks and generates responses using Google Gemini.

### Query the RAG Pipeline

Modify or run `App.py` for interactive querying:

```powershell
python App.py
```

## Project Structure

```
rag-pipeline/
├── README.md                      # This file
├── .env.example                   # Example environment variables (copy to .env)
├── .gitignore                     # Git ignores (.env, venv/, __pycache__/, etc.)
├── LICENSE                        # MIT License
├── requirements.txt               # Python dependencies
│
├── load_pdf.py                    # Loads PDF using PyPDF loader
├── chunk_pdf.py                   # Splits documents into chunks (RecursiveCharacterTextSplitter)
├── embeddings.py                  # Calls Google embedding model (gemini-embedding-001)
├── vector_store.py                # ChromaDB integration and persistence
├── rag.py                         # Orchestrates retrieval + generation pipeline
├── App.py                         # Interactive application / demo
│
├── network.pdf                    # Sample PDF for testing
└── .github/
    └── workflows/
        └── python-ci.yml          # GitHub Actions CI workflow
```

## How the RAG Pipeline Works

### Step-by-Step Flow

1. **PDF Loading** (`load_pdf.py`)
   - Loads a PDF file using `PyPDFLoader` from LangChain
   - Converts each page to text

2. **Text Chunking** (`chunk_pdf.py`)
   - Uses `RecursiveCharacterTextSplitter` to split documents
   - Default: 500 characters per chunk, 50-character overlap
   - Overlap preserves context at chunk boundaries

3. **Embedding Generation** (`embeddings.py`)
   - Sends each chunk to `gemini-embedding-001` API
   - Generates 768-dimensional vector embeddings
   - Embeddings capture semantic meaning of text

4. **Vector Indexing** (`vector_store.py`)
   - Stores embeddings in ChromaDB (vector database)
   - Enables fast similarity-based retrieval
   - Persists to disk for future queries

5. **Retrieval** (`rag.py`)
   - User submits a query
   - Query is converted to an embedding
   - ChromaDB returns top-k most similar chunks

6. **Prompt Assembly**
   - Retrieved chunks + user query → construct context-rich prompt
   - Prompt instructs Gemini to answer using retrieved context

7. **Generation** (`rag.py`)
   - Sends prompt to `gemini-2.5-flash` LLM
   - Model generates response grounded in retrieved documents

8. **Response**
   - Final response is returned to user
   - Contains only information supported by the source PDF

### Example Flow

```
User Query: "What is IPv4?"
     ↓
Embed Query → "What is IPv4?" → [embedding vector]
     ↓
Search ChromaDB → Retrieve top 3 chunks about IPv4
     ↓
Build Prompt: "Using the following context: [chunks], answer: What is IPv4?"
     ↓
Call Gemini API → Generate answer
     ↓
Return: "IPv4 stands for Internet Protocol Version 4..."
```

## Security Best Practices

### Protecting Your API Key

**Never commit your API key to version control.**

- **Use `.env` file locally** — Store your `GOOGLE_API_KEY` in `.env` (already in `.gitignore`)
- **Never hardcode secrets** — Don't write keys directly in Python files or notebooks
- **Use short-lived credentials** — Rotate API keys regularly and use restricted scopes when possible

### For GitHub Actions / CI

If you deploy this project with CI/CD:

1. Go to your GitHub repository → **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Add `GOOGLE_API_KEY` with your actual key
4. In workflow files, reference it as:
   ```yaml
   env:
     GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
   ```

### For Collaboration

- Share credentials via a secure secret manager (e.g., 1Password, LastPass, AWS Secrets Manager)
- Never email or Slack API keys
- If a key is exposed, regenerate it immediately on Google Cloud Console

## Dependencies

See `requirements.txt` for the complete list:

- **langchain** — Framework for building LLM applications
- **langchain-community** — Community integrations (PDF loaders, embeddings, etc.)
- **langchain-text-splitters** — Text splitting utilities
- **python-dotenv** — Load environment variables from `.env`
- **numpy** — Numerical computing

## Troubleshooting

### `ModuleNotFoundError: No module named 'langchain_community'`
Ensure the virtual environment is activated and dependencies are installed:
```powershell
& "venv\Scripts\Activate.ps1"
python -m pip install -r requirements.txt
```

### `ValueError: File path ... is not a valid file or url`
Verify the PDF file exists in the project directory and the path in your script matches.

### `GOOGLE_API_KEY not found`
- Check that `.env` file exists and contains `GOOGLE_API_KEY=your_key`
- Verify `python-dotenv` is installed
- Ensure you're running from the project root directory

### API quota exceeded
Google Generative AI has free-tier rate limits. Monitor your usage at [Google AI Studio](https://makersuite.google.com/app/apikey).

## Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Google Generative AI Python SDK](https://ai.google.dev/tutorials/python_quickstart)
- [RAG Explained](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/)

## Built for Learning

This repository is a hands-on demonstration of RAG principles and how to integrate AI models, embeddings, and vector databases. It's designed for:

- **Students** learning about RAG and LLM architectures
- **Developers** building their first AI applications
- **Teams** exploring Google Gemini and LangChain

**Not recommended for production use without:**
- Error handling and input validation
- API rate limiting and caching
- Authentication and authorization
- Monitoring and observability
- Cost controls and quotas

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Found a bug or want to improve the code? Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## Support

- **Issues** — Use GitHub Issues to report bugs or request features
- **Discussions** — Ask questions in GitHub Discussions
- **Email** — Contact via repository maintainer

---
