# 🚀 Getting Started with TrustLayer-AI

This guide walks you through setting up, configuring, and running **TrustLayer-AI** locally on Windows, macOS, or Linux.

---

## 📋 System Prerequisites

Ensure you have the following installed on your machine:
- **Python**: Version `3.10` or higher (`python --version`)
- **Node.js**: Version `18.17` or higher (`node --version`)
- **npm**: Version `9.0` or higher (`npm --version`)
- **Ollama** (Optional, recommended for AI text synthesis): [https://ollama.com](https://ollama.com)
- **Git**: [https://git-scm.com](https://git-scm.com)

---

## 🛠️ Step-by-Step Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/TrustLayer-AI.git
cd TrustLayer-AI
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# On Linux / macOS
cp .env.example .env

# On Windows (cmd / PowerShell)
copy .env.example .env
```

Review and adjust settings in `.env` as needed:
```env
DATA_BACKEND=csv
VECTOR_BACKEND=chroma
LLM_PROVIDER=ollama
OLLAMA_ENDPOINT=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:7b-instruct
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 3. Set Up Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux / macOS:
source venv/bin/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (cmd):
.\venv\Scripts\activate.bat

# Install backend dependencies
pip install -r requirements.txt
```

### 4. Set Up Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### 5. (Optional) Pull LLM Model with Ollama
If you want to enable grounded AI narrative generation:
```bash
ollama serve
ollama pull qwen2.5:7b-instruct
```

### 6. Build Vector Embeddings (Initial Setup)
Generate local ChromaDB embeddings from the canonical dataset (`data/rag/`):
```bash
python run.py --build-vectors
```

---

## 🏃 Running the Application

### Single Command Orchestrator (Backend + Frontend)
```bash
python run.py
```
- **Web App**: [http://localhost:3000](http://localhost:3000)
- **FastAPI Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Individual Service Execution
- **Run Backend only**:
  ```bash
  python run.py --backend
  ```
- **Run Frontend only**:
  ```bash
  python run.py --frontend
  ```
- **Run System Doctor / Health Diagnostics**:
  ```bash
  python run.py --doctor
  ```

---

## 🐳 Docker Quickstart

If you prefer running via Docker Compose:
```bash
docker-compose up --build
```
This builds and starts both the FastAPI gateway and Next.js frontend with proper environment binding.

---

## 🧪 Running Tests

Execute the automated Pytest test suite:
```bash
python run.py --test
# or
pytest
```
