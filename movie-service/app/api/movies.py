import logging

from fastapi import APIRouter, HTTPException

from app.api.models import MovieIn, MovieOut, MovieUpdate
from app.api import db_manager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('movies.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

movies = APIRouter()


@movies.get('/', response_model=list[MovieOut])
async def index():
    return await db_manager.get_all_movies()


@movies.get('/{id}', response_model=MovieOut)
async def index(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@movies.post('/', status_code=201)
async def add_movie(payload: MovieIn):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with id:{cast_id} not found")

    movie_id = await db_manager.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.model_dump()
    }

    logger.info(payload)

    return response


@movies.put('/{id}')
async def update_movie(id: int, payload: MovieUpdate):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.model_dump(exclude_unset=True)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.model_copy(update=update_data)

    return await db_manager.update_movie(id, updated_movie)


@movies.delete('/{id}')
async def delete_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return await db_manager.delete_movie(id)
