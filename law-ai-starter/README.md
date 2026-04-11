# Law AI Starter Scaffold

This is a professional MVP starter scaffold for a **Law AI web application**.

It is split into two parts:
- `frontend/` — Next.js + TypeScript website
- `backend/` — FastAPI backend for chat, legal retrieval, and admin APIs

## What this scaffold already includes
- Homepage starter
- Chat page starter
- Admin page starter
- Shared frontend components
- Backend API structure
- Mock legal chat response with citations
- Mock officer authority lookup endpoint
- Environment variable examples
- Clean folder structure for future expansion

## What this scaffold does NOT include yet
- Real authentication
- Real payment/subscription system
- Real database connection
- Real OpenAI integration
- Real vector search / legal retrieval pipeline
- Production deployment configuration

## Recommended build order
1. Run frontend and backend locally
2. Confirm homepage and chat UI load
3. Confirm chat page can call backend
4. Replace mocked chat service with real LLM + retrieval
5. Add PostgreSQL + models
6. Add admin authentication
7. Add admin upload / legal data management

## Frontend setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:
- `http://localhost:3000`

## Backend setup
```bash
cd backend
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend runs on:
- `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

## Environment variables
Copy these files and fill them later:
- `frontend/.env.example`
- `backend/.env.example`

## First task after scaffold
Your first real implementation target should be:
- make the chat page call the backend successfully
- replace mock answers with real legal information retrieval
