from pydantic import BaseModel


class BaseArticleSchema(BaseModel):
    title: str
    description: str


class ArticleSchema(BaseArticleSchema):
    title: str
    description: str

    class Config:
        orm_mode = True
