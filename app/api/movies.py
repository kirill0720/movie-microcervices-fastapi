import logging

from fastapi import APIRouter, HTTPException

from app.api.models import Movie

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('movies.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

fake_movie_db = [
    {
        'name': 'Star Wars: Episode IX - The Rise of Skywalker',
        'plot': 'The surviving members of the resistance face the First Order once again.',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Daisy Ridley', 'Adam Driver']
    }
]

movies = APIRouter()


@movies.get('/', response_model=list[Movie])
async def index():
    return fake_movie_db


@movies.post('/movies', status_code=201)
async def add_movie(payload: Movie):
    logger.info(payload)
    movie = payload.model_dump()
    fake_movie_db.append(movie)
    return {'id': len(fake_movie_db) - 1}


@movies.put('/movies/{movie_id}')
def update_movie(movie_id: int, payload: Movie):
    if 0 <= movie_id < len(fake_movie_db):
        movie = payload.model_dump()
        fake_movie_db[movie_id] = movie
        return None
    raise HTTPException(status_code=404, detail='Movie with given id not found')


@movies.delete('/movies/{movie_id}')
def delete_movie(movie_id: int):
    if 0 <= movie_id < len(fake_movie_db):
        del fake_movie_db[movie_id]
        return None
    raise HTTPException(status_code=404, detail='Movie with given id not found')
