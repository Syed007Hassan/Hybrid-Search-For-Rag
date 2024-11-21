"""
This file is responsible for routing the incoming requests to the respective endpoints.
"""

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from services.chat import ChatService
from models.company import Company
from services.embedding import Embedding
from models.database import get_db_session

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")
chat_service = ChatService()
embedding_util = Embedding()


class ChatRequest(BaseModel):
    """
    This class is used to model the request for the chat endpoint.
    """

    query: str


class CompanyCreate(BaseModel):
    name: str
    description: str
    industry: str
    size: str
    location: str


class SearchRequest(BaseModel):
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


@api_router.post("/companies")
async def add_company(company: CompanyCreate):
    content = f"{company.name}\n{company.description}\n{company.industry}\n{company.size}\n{company.location}"
    embedding = embedding_util.generate(content)
    
    new_company = Company(
        name=company.name,
        description=company.description,
        industry=company.industry,
        size=company.size,
        location=company.location,
        content=content,
        embedding=embedding
    )
    
    with get_db_session() as session:
        session.add(new_company)
        session.commit()
    return {"message": "Company added successfully"}


@api_router.post("/search-company", response_class=JSONResponse)
async def search_company(search_request: SearchRequest):
    response, company_recommendations = chat_service.generate_response(
        search_request.query
    )
    return {
        "response": response,
        "company_recommendations": [
            company.to_dict() for company in company_recommendations
        ],
    }
