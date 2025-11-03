"""FastAPI application that exposes the ImunizaChat RAG agent through a REST endpoint."""

import asyncio
import uuid
from dataclasses import dataclass, field
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pydantic_ai.messages import ModelMessage

from rag_agent import agent, RAGDeps
from utils import get_chroma_client


@dataclass
class SessionState:
    """Holds the conversation history for a single chat session."""

    messages: List[ModelMessage] = field(default_factory=list)


class ChatRequest(BaseModel):
    """Body schema for the chat endpoint."""

    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    """Response schema for the chat endpoint."""

    reply: str
    session_id: str


app = FastAPI(title="ImunizaChat API", version="1.0.0")

# Allow local development tools (e.g. file:// frontends) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global dependencies shared by all sessions
agent_deps = RAGDeps(
    chroma_client=get_chroma_client("./chroma_db"),
    collection_name="docs",
    embedding_model="all-MiniLM-L6-v2",
)

# In-memory session store with per-session locks for concurrency safety
_sessions: Dict[str, SessionState] = {}
_session_locks: Dict[str, asyncio.Lock] = {}
_sessions_lock = asyncio.Lock()


async def _get_session_lock(session_id: str) -> asyncio.Lock:
    """Return a lock for the provided session id, creating it if needed."""

    async with _sessions_lock:
        if session_id not in _session_locks:
            _session_locks[session_id] = asyncio.Lock()
        return _session_locks[session_id]


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint."""

    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat with the ImunizaChat agent.

    A session id is returned on the first call and should be reused on subsequent
    messages to maintain the conversation context.
    """

    session_id = request.session_id or str(uuid.uuid4())
    session_lock = await _get_session_lock(session_id)

    async with session_lock:
        session = _sessions.setdefault(session_id, SessionState())

        try:
            result = await agent.run(
                request.message,
                deps=agent_deps,
                message_history=session.messages,
            )
        except Exception as exc:  # pragma: no cover - defensive
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        session.messages.extend(result.new_messages())

    return ChatResponse(reply=result.data, session_id=session_id)


__all__ = ["app"]
