from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class Article(Base):
    __tablename__ = "articles"

    id        = Column(Integer, primary_key=True, index=True)
    title     = Column(String(255), nullable=False)
    slug      = Column(String(255), unique=True, nullable=False)
    category  = Column(String(100))          # vd: "thi công", "vật liệu"
    content   = Column(Text, nullable=False)
    thumbnail = Column(String(500))          # URL ảnh
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())