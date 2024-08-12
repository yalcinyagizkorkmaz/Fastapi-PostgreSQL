from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List,Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session

# FastAPI uygulamasını oluştur
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Pydantic modelini tanımla
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]  # 'choice' yerine 'choices' olarak düzelttim


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

@app.post("/questions/")
async def create_questions(question: QuestionBase,db:db_dependency):
    
    db_question=models.Question(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice=models.Choices(choice_text=choice.choice_text,is_correct=choice.is_correct,question_id=db_question.id)
        db.add(db_choice)
    db.commit()

@app.get("/questions/{question_id}")
async def get_question(question_id: int, db: db_dependency):
    # Verilen ID'ye sahip soruyu al
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Soruya bağlı seçenekleri al
    choices = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    
    # Sonuçları döndür
    return {
        "question_text": question.question_text,
        "choices": [
            {"choice_text": choice.choice_text, "is_correct": choice.is_correct}
            for choice in choices
        ]
    }

@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Choices not found')
    return result

