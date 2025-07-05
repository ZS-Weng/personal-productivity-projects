from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class PomodoroSession(Base):
    """
    Model to store completed pomodoro sessions
    """
    __tablename__ = "pomodoro_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    pomodoros_completed = Column(Integer, nullable=False, default=0)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<PomodoroSession(id={self.id}, pomodoros={self.pomodoros_completed}, year={self.year}, month={self.month})>"