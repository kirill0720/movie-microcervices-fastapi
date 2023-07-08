from pydantic import BaseModel


class Movie(BaseModel):
    name: str
    plot: str | None = None
    genres: list[str]
    casts: list[str]
