# 🐙 GitHub Upload & Repository Details Guide

This guide contains all the exact metadata, description, topics, and terminal commands needed to upload **TrustLayer-AI** to GitHub.

---

## 📌 Recommended GitHub Repository Details

When creating your repository on GitHub ([https://github.com/new](https://github.com/new)), use the following suggested details:

| Field | Recommended Value |
| :--- | :--- |
| **Repository Name** | `TrustLayer-AI` *(or `trustlayer-ai`)* |
| **Description** | `🏨 Grounded, Explainable & Anti-Hallucinatory AI Hotel Recommendation Engine with 5D Aspect-Based Sentiment Analysis (FastAPI + Next.js 16 + ChromaDB / PostgreSQL + Ollama)` |
| **Visibility** | **Public** *(recommended)* or **Private** |
| **Initialize with README** | **Unchecked** *(already created locally)* |
| **Add .gitignore** | **None** *(already configured locally)* |
| **Choose a license** | **None** *(MIT License already added)* |

### 🏷️ Recommended GitHub Topics (Tags)
Copy and paste these tags into the "Topics" section of your GitHub repository page:
```text
python, fastapi, nextjs, rag, llm, anti-hallucination, aspect-based-sentiment-analysis, hotel-recommendation, vector-search, chromadb, ollama, pgvector, grounding, explainable-ai, tailwindcss, artificial-intelligence, machine-learning, information-retrieval
```

---

## 💻 Step-by-Step Terminal Commands to Push to GitHub

Open PowerShell or Terminal in the root project directory (`d:\Side_Projects\0_Independent_Project\NewBackend_start`):

### 1. Initialize Git Repository
```bash
git init
```

### 2. Verify `.gitignore` is Active
Make sure virtual environments, cache files, and node_modules are ignored:
```bash
git status
```

### 3. Stage All Tracked Files
```bash
git add .
```

### 4. Create the Initial Commit
```bash
git commit -m "feat: initial commit - TrustLayer-AI hotel recommendation engine"
```

### 5. Set Default Branch to `main`
```bash
git branch -M main
```

### 6. Link Your GitHub Remote Repository
*(Replace `YOUR_GITHUB_USERNAME` and `TrustLayer-AI` with your GitHub username and repository name)*
```bash
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/TrustLayer-AI.git
```

### 7. Push to GitHub
```bash
git push -u origin main
```

---

## 🔑 Authentication Note (If prompted for password)

GitHub no longer accepts account passwords for command-line Git operations. You can authenticate using either:
1. **GitHub CLI (`gh`)**:
   ```bash
   gh auth login
   ```
2. **Personal Access Token (Classic or Fine-Grained)**:
   - Go to: [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)
   - Generate token with `repo` scope.
   - Use the token as your password when Git prompts for credentials.
3. **SSH Key**:
   - Add your SSH public key to [GitHub SSH Keys](https://github.com/settings/keys)
   - Use the SSH remote URL:
     ```bash
     git remote set-url origin git@github.com:YOUR_GITHUB_USERNAME/TrustLayer-AI.git
     git push -u origin main
     ```

---

## 📦 What is Included in the Upload?

- ✅ **Full FastAPI Backend** (`app/`)
- ✅ **Next.js 16 UI Frontend** (`frontend/` - excludes `node_modules` and `.next`)
- ✅ **Canonical Dataset & Knowledge Documents** (`data/exports/`, `data/rag/`)
- ✅ **Master Ingestion & Pipeline Scripts** (`scripts/`)
- ✅ **Automated Test Suite** (`tests/`)
- ✅ **Documentation Hub** (`docs/`, `architecture_and_system_docs/`)
- ✅ **LaTeX Research Paper & Reports** (`latext_files/`)
- ✅ **Unified CLI Runner & Docker Setup** (`run.py`, `Dockerfile`, `docker-compose.yml`)
- ❌ **Excluded via `.gitignore`**: `.env` secrets, `__pycache__`, `node_modules`, `.pytest_cache`, generated `.sqlite3` vector stores, and test databases.
