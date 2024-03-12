from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import func


class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(length=50), nullable=False)
    content = Column(String, nullable=False)
    publish = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    publish_at = Column(DateTime)