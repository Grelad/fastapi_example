from http import HTTPStatus
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from . import models
from .database import engine, sessionLocal
from .schemas import ArticleSchema, BaseArticleSchema

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return {"message": "Index page"}


@app.get("/articles/", response_model=List[ArticleSchema])
async def get_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return articles


@app.get(
    "/articles/{id}/", status_code=status.HTTP_200_OK, response_model=ArticleSchema
)
async def article_details(id: int, db: Session = Depends(get_db)) -> Any:
    article = db.query(models.Article).get(id)
    if article:
        return article

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="The article does not exist"
    )


@app.post("/articles/", status_code=status.HTTP_201_CREATED)
async def add_article(
    article: BaseArticleSchema, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    new_article = models.Article(title=article.title, description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@app.put("/articles/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_article(
    id: int, article: BaseArticleSchema, db: Session = Depends(get_db)
):
    db.query(models.Article).filter(models.Article.id == id).update(
        {"title": article.title, "description": article.description}
    )
    db.commit()
    return {"message": "The article is updated"}


@app.delete("/articles/{id}")
async def delete_article(id: int, db: Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).delete(
        synchronize_session=False
    )
    db.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)
