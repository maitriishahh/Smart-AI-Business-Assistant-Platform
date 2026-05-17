# AI Business Assistant Platform

An AI-powered business operations assistant built with FastAPI, React, LangGraph, MongoDB, and RAG pipelines.

The platform helps businesses automate customer interaction workflows using conversational AI, document retrieval, lead management, CRM sync, workflow automations, and operational analytics.

---

# Demo Video


[Demo Video](https://drive.google.com/file/d/1xgjWuqeEA3J0-e_KKxHxNmmKC30Z3Qvy/view?usp=sharing)



---
# Features

## AI Chat Assistant

- Multi-turn AI conversations
- Context-aware responses
- Business-oriented assistant behavior
- Conversational memory support
- AI fallback handling
- Retrieval-Augmented Generation (RAG)

---

# RAG Pipeline

- PDF upload support
- Semantic chunking
- Embedding-based retrieval
- Contextual answers from uploaded documents
- Reduced hallucinations using retrieval context
- User-specific document retrieval

---

# Memory System

## Short-Term Memory

- Maintains recent conversational context
- Supports multi-turn interactions
- Improves conversational continuity

## Long-Term Memory

- MongoDB-based persistent memory
- Stores previous conversations
- Personalized AI interactions

---

# AI Fallback Architecture

The platform uses a primary + fallback LLM architecture for reliability.

## Primary Model
- Gemini API

## Fallback Model
- Groq API

## Workflow

```text
User Query
↓
Gemini Response Attempt
↓
If Gemini Fails
↓
Automatically Switch to Groq
↓
Return AI Response
```

This improves:
- system reliability
- response continuity
- production readiness
- fault tolerance

---

# Multi-Agent Workflow

The platform uses LangGraph-based orchestration with multiple AI agents.

## Planner Agent

Responsibilities:
- Understands user intent
- Plans task execution
- Decides workflow routing
- Handles orchestration logic

---

## Executor Agent

Responsibilities:
- Executes AI tasks
- Generates business responses
- Handles RAG-based answering
- Performs workflow actions

---

## Validator / Critic Agent

Responsibilities:
- Validates generated responses
- Reduces hallucinations
- Ensures response quality
- Performs output verification

---

# Lead Management

- Lead intent detection
- Multi-step lead collection
- CRM synchronization
- AI-generated follow-up emails
- Lead storage in MongoDB

---

# Workflow Automations

## 1. Email Summarization

Features:
- Email summarization
- Urgency detection
- Action item extraction
- Suggested reply generation

---

## 2. Follow-Up Generation

Features:
- AI-generated business follow-up emails
- Personalized communication
- Sales outreach automation

---

## 3. CRM Sync

Features:
- CRM lead storage
- MongoDB synchronization
- CSV export support
- Operational tracking

---

# Dashboard

## Dashboard Page

Main operational control panel for:
- running automations
- viewing CRM records
- managing workflows

### Includes:
- Email summarization panel
- CRM sync form
- Follow-up generation form
- CRM records section

---

## Analytics Page

Displays:
- Total leads
- Total conversations
- Uploaded documents
- CRM sync counts
- Automation execution counts

---

## Chat Assistant Page

Features:
- AI chat interface
- PDF upload support
- RAG interactions
- Memory-enabled conversations

---

## Leads Page

Displays:
- Captured leads
- Lead details
- Company information
- Requirements
- Timestamps

---

## Documents Page

Displays:
- Uploaded PDFs
- Original filenames
- Upload timestamps
- Document management records

---

## Chat Logs Page

Displays:
- User messages
- AI responses
- Conversation history
- Operational logs

---

# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js + Tailwind CSS |
| Backend | FastAPI |
| Database | MongoDB |
| AI Models | Gemini + Groq |
| Agent Orchestration | LangGraph |
| Vector Retrieval | ChromaDB / FAISS |
| Authentication | JWT |

---

# Project Structure

```text
AI Biz Assistant Platform/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── automations/
│   │   ├── config/
│   │   ├── database/
│   │   ├── memory/
│   │   ├── rag/
│   │   ├── services/
│   │   ├── uploads/
│   │   ├── workflows/
│   │   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│
├── requirements.txt
├── package.json
├── README.md
└── .env.example
```

---

# Installation

## Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn backend.app.main:app --reload
```

Backend runs on:

```text
http://localhost:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# Environment Variables

Create a `.env` file:

```env
MONGODB_URL=
DATABASE_NAME=

SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

GEMINI_API_KEY=

GROQ_API_KEY=
```

---

# Example Workflow

```text
Upload PDF
↓
Ask Questions
↓
RAG Retrieval
↓
AI Response
↓
Lead Detection
↓
Lead Capture
↓
CRM Sync
↓
AI Follow-Up Generation
↓
Analytics & Logs
```

---

# Available Modules

- Authentication System
- RAG Document Assistant
- Memory Management
- Multi-Agent Workflow
- Lead Capture
- CRM Sync
- Email Summarization
- Follow-Up Automation
- Analytics Dashboard
- Chat Logs
- Document Management

---

# Workflow Testing

## Authentication Test

### Login Input

| Field | Value |
|---|---|
| Email | moksha@example.com |
| Password | 321 |

Expected:
- Successful login
- Redirect to dashboard

---

## RAG Testing

Upload a PDF and ask:

```text
What services are mentioned in the PDF?
```

Expected:
- AI retrieves answers from uploaded document

---

## Memory Testing

Input:

```text
My startup name is NovaMind Labs
```

Then ask:

```text
What company name did I mention?
```

Expected:
- AI remembers previous context

---

## Lead Detection Testing

Input:

```text
I want to book a consultation for AI automation
```

Expected:
- Lead workflow triggered

---

## CRM Sync Testing

Fill CRM form:

| Field | Example |
|---|---|
| Name | Michael Lee |
| Email | michael@brightcore.io |
| Company | BrightCore |
| Phone | 9876543210 |
| Requirements | Workflow automation |
| Priority | Medium |

Expected:
- CRM sync success
- Record visible in dashboard

---

## Email Summary Testing

Paste sample email:

```text
Hello Team,

The client requested final updates for the analytics dashboard before Thursday.

Please complete:
- UI fixes
- deployment setup
- chatbot testing

Priority is high because the demo is scheduled Friday morning.
```

Expected:
- Summary generated
- Action items extracted
- Urgency detected

---

## Follow-Up Automation Testing

Generate AI follow-up email using dashboard form.

Expected:
- Professional follow-up email generated

---

# Demo Flow

```text
Login
↓
Upload PDF
↓
Ask RAG Questions
↓
AI retrieves contextual answers
↓
Lead detected
↓
Lead captured
↓
CRM sync automation
↓
Follow-up generation
↓
Analytics updated
↓
Logs and documents tracked
```

---



# Future Improvements

- Docker deployment
- Cloud hosting
- Google Calendar integration
- Zoom integration
- Streaming responses
- Voice interaction
- Redis caching

---

# Notes

The project is fully functional in local development mode.

Cloud deployment and Dockerization were planned but not completed due to time constraints.
