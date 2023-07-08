from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

fake_movie_db = [
    {
        'name': 'Star Wars: Episode IX - The Rise of Skywalker',
        'plot': 'The surviving members of the resistance face the First Order once again.',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Daisy Ridley', 'Adam Driver']
    }
]


class Movie(BaseModel):
    name: str
    plot: str | None = None
    genres: list[str]
    casts: list[str]


@app.get('/', response_model=list[Movie])
async def index():
    return fake_movie_db
