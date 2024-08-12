from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List

# FastAPI uygulamasını oluştur
app = FastAPI()

# Pydantic modelini tanımla
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]  # 'choice' yerine 'choices' olarak düzelttim

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
