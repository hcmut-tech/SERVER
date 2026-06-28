from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from database import Base, engine, get_db
from models import Article
import unicodedata
import re

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BK ARCH API", version="1.0.0")

# Cho phép hcmut.pages.dev gọi API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hcmut.pages.dev",
        "https://server-6baj.onrender.com",
        "http://127.0.0.1:5500",   # Live Server local dev
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hàm tự động tạo slug từ tiêu đề
def create_slug(title: str) -> str:
    # Chuyển tiếng Việt có dấu → không dấu
    title = unicodedata.normalize('NFD', title)
    title = ''.join(c for c in title if unicodedata.category(c) != 'Mn')
    # Chuyển thành chữ thường, thay khoảng trắng bằng dấu gạch
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s-]', '', title)
    title = re.sub(r'\s+', '-', title.strip())
    return title

# Cấu trúc dữ liệu bài viết
class ArticleInput(BaseModel):
    title: str
    category: Optional[str] = None
    content: str
    thumbnail: Optional[str] = None

# Lấy danh sách bài viết
@app.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

# Lấy 1 bài viết theo ID
@app.get("/articles/{id}")
def get_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    return article

# Tạo bài viết mới
@app.post("/articles")
def create_article(data: ArticleInput, db: Session = Depends(get_db)):
    slug = create_slug(data.title)
    article = Article(
        title=data.title,
        slug=slug,
        category=data.category,
        content=data.content,
        thumbnail=data.thumbnail
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

# Sửa bài viết
@app.put("/articles/{id}")
def update_article(id: int, data: ArticleInput, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    article.title = data.title
    article.slug = create_slug(data.title)
    article.category = data.category
    article.content = data.content
    article.thumbnail = data.thumbnail
    db.commit()
    return article

# Xóa bài viết
@app.delete("/articles/{id}")
def delete_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    db.delete(article)
    db.commit()
    return {"message": "Đã xóa bài viết thành công"}

@app.get("/articles/slug/{slug}")
def get_article_by_slug(slug: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    return article