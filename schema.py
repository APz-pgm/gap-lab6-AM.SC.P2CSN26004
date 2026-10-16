from __future__ import annotations
import json, re
from pathlib import Path
from pydantic import BaseModel, Field
import security

class Question(BaseModel):
    topic: str = Field(min_length=3, max_length=200)
    text: str = Field(min_length=15, max_length=1000)
    source: str = Field(min_length=1, max_length=300)

class Reply(BaseModel):
    questions: list[Question] = Field(min_length=1, max_length=5)

