from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Numeric(10, 2), nullable=False)

    description = Column(String, nullable=True)

    category = Column(String, nullable=False)

    date = Column(Date, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    owner = relationship("User", back_populates="expenses")
    