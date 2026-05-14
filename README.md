[![Python CI](https://github.com/syedalamshah/rag-pipeline/actions/workflows/python-ci.yml/badge.svg)](https://github.com/syedalamshah/rag-pipeline/actions)

RAG Pipeline
============

Simple Python Retrieval-Augmented Generation (RAG) pipeline.

Files of interest:
- `load_pdf.py` — load PDF into LangChain loader.
- `chunk_pdf.py` — split loaded PDF into chunks.
- `embeddings.py`, `vector_store.py`, `rag.py` — RAG pipeline components.

Setup
-----
1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
& "venv\Scripts\Activate.ps1"
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Copy the example environment file and set your API key:

```powershell
copy .env.example .env
# then edit .env and set GOOGLE_API_KEY
```

Usage
-----
- Split the PDF into chunks:

```powershell
python chunk_pdf.py
```

- Load the PDF:

```powershell
python load_pdf.py
```

Notes
-----
- Do not commit secrets. Add your API keys to `.env` (which is ignored).
- The repository already includes a sample `network.pdf` used by the demo scripts.
