from typing import List

from app.utils.index import HealthUtil
from fastapi import APIRouter, Depends, HTTPException, status
from llama_index.core.llms import ChatMessage, MessageRole
from pydantic import BaseModel
util = HealthUtil()
agent_executor = util.get_agent()
chat_router = r = APIRouter()


class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]


class _Result(BaseModel):
    result: _Message

@r.post("")
async def chat(
    data: _ChatData,
) -> _Result:
    # check preconditions and get last message
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    lastMessage = data.messages.pop()
    if lastMessage.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )
    # convert messages coming from the request to type ChatMessage
    messages = [
        ChatMessage(
            role=m.role,
            content=m.content,
        )
        for m in data.messages
    ]

    # query chat engine
    response = agent_executor.run(input=lastMessage.content)
    return _Result(
        result=_Message(role=MessageRole.ASSISTANT, content=response)
    )