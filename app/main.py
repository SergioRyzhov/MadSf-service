from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, models, schemas
from .database import get_db, init_db
from .config import settings
from media_service.s3 import upload_image

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/memes", response_model=list[schemas.Meme])
async def read_memes(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    memes = await crud.get_memes(db, skip=skip, limit=limit)
    return memes


@app.get("/memes/{id}", response_model=schemas.Meme)
async def read_meme(id: int, db: AsyncSession = Depends(get_db)):
    meme = await crud.get_meme(db, meme_id=id)
    if meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme


@app.post("/memes", response_model=schemas.Meme)
async def create_meme(title: str, description: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    filename = file.filename
    image_url = upload_image(file.file, filename)
    meme = schemas.MemeCreate(title=title, description=description)
    return await crud.create_meme(db, meme, image_url=image_url)


@app.put("/memes/{id}", response_model=schemas.Meme)
async def update_meme(id: int, meme: schemas.MemeUpdate, db: AsyncSession = Depends(get_db)):
    updated_meme = await crud.update_meme(db, meme_id=id, meme=meme)
    if updated_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return updated_meme


@app.delete("/memes/{id}", response_model=schemas.Meme)
async def delete_meme(id: int, db: AsyncSession = Depends(get_db)):
    deleted_meme = await crud.delete_meme(db, meme_id=id)
    if deleted_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return deleted_meme
