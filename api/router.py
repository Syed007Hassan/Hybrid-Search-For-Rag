"""
This file is responsible for routing the incoming requests to the respective endpoints.
"""

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from services.chat import ChatService

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")
chat_service = ChatService()


class ChatRequest(BaseModel):
    """
    This class is used to model the request for the chat endpoint.
    """

    query: str


@api_router.get("/")
async def tester(request: Request):
    """
    This function is used to test the chatbot.
    """
    return templates.TemplateResponse("chat.html", {"request": request})


@api_router.post("/chat", response_class=JSONResponse)
async def chat(chat_request: ChatRequest):
    """
    This function is used to chat with the chatbot.
    """
    response, product_recommendations = chat_service.generate_response(
        chat_request.query
    )
    return {
        "response": response,
        "product_recommendations": [
            product.to_dict() for product in product_recommendations
        ],
    }
