from fastapi import APIRouter, HTTPException, status, Body
from sse_starlette.sse import EventSourceResponse
from app.schemas.chat import ChatInput, ChatOutputChunk
from app.services.chat_service import chat_service

router = APIRouter()