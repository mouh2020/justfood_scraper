from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

class Article(SQLModel, table=True):
    id              : Optional[int]     = Field(default=None, primary_key=True)
    article_id      : int
    title           : Optional[str]     = Field(default=None)
    article_text           : Optional[str]     = Field(default=None)
    article_html           : Optional[str]     = Field(default=None)

sqlite_file_name = "justfood_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)