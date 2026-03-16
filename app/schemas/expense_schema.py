from __future__ import annotations


from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0)
    category: str
    description: str | None = None
    date: date


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str | None
    date: date
    created_at: datetime

    model_config = {"from_attributes": True}


class ExpenseUpdate(BaseModel):
    amount: float | None = Field(default=None, gt=0)
    category: str | None = None
    description: str | None = None
    date: Optional[date] = None
