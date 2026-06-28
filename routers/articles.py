from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Article

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("/")
def get_articles(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Article).offset(skip).limit(limit).all()

@router.get("/{slug}")
def get_article(slug: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    return article

@router.post("/")
def create_article(data: dict, db: Session = Depends(get_db)):
    article = Article(**data)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

@router.put("/{id}")
def update_article(id: int, data: dict, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    for key, value in data.items():
        setattr(article, key, value)
    db.commit()
    return article

@router.delete("/{id}")
def delete_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    db.delete(article)
    db.commit()
    return {"message": "Đã xóa"}