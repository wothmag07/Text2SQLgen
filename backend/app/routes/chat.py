from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.text2sql import Text2SQLAgent
from app.database import get_schema

router = APIRouter(prefix="/api")

agent = Text2SQLAgent()


class ChatRequest(BaseModel):
    message: str
    history: list[list[str]] = []


class ChatResponse(BaseModel):
    response: str
    sql: str | None = None
    columns: list[str] = []
    results: list[list] = []
    error: str | None = None


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    history_tuples = [(h[0], h[1]) for h in request.history if len(h) == 2]
    result = agent.run(request.message, history_tuples)
    return ChatResponse(**result)


@router.get("/schema")
def schema():
    try:
        return {"schema": get_schema()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suggestions")
def suggestions():
    return {
        "suggestions": [
            "How many patients are there in total across all tables?",
            "What is the average BMI of diabetic patients?",
            "List the top 10 countries with the highest heart attack risk",
            "How many breast cancer patients received irradiation?",
            "What is the average age of glaucoma patients by type?",
            "Show the distribution of liver cirrhosis stages",
            "Which patients have both diabetes and high blood pressure?",
            "What percentage of heart attack patients are smokers?",
        ]
    }
