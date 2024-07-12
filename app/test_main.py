import asyncio
import io

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

title = "Test Meme"
description = "This is a test meme"
file_content = b"fake image data"
file = io.BytesIO(file_content)
file.name = "test_image.jpg"
created_meme_id = 0

data = {
    "title": title,
    "description": description,
    "file": (file, "test_image.jpg")
}


@pytest.fixture(scope="module")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(init_db)
    async with TestingSessionLocal() as session:
        yield session
    await engine.dispose()


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def client(db_session: AsyncSession, event_loop):
    async with TestClient(app) as c:
        yield c


@pytest.mark.asyncio
async def test_read_memes(client: TestClient, db_session: AsyncSession):

    async with AsyncClient(app=app, base_url="http://test", timeout=None) as ac:
        response = await ac.get("/memes")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_meme(client: TestClient, db_session: AsyncSession):
    global created_meme_id

    async with AsyncClient(app=app, base_url="http://test", timeout=None) as ac:
        response = await ac.post(
            "/memes",
                files={"file": file},
                params={"title": data["title"], "description": data["description"]}
        )

    assert response.status_code == 200
    json_response = response.json()
    created_meme_id = json_response["id"]

    assert json_response["title"] == title
    assert json_response["description"] == description
    assert "image_url" in json_response
    assert json_response["image_url"].startswith("http://minio:9000/memes/")


@pytest.mark.asyncio
async def test_read_meme(client: TestClient, db_session: AsyncSession):

    async with AsyncClient(app=app, base_url="http://test", timeout=None) as ac:
        response = await ac.get("/memes/1")
    assert response.status_code == 200
    read_meme = response.json()
    assert read_meme["id"] == 1
    assert read_meme["title"] == data["title"]
    assert read_meme["description"] == data["description"]
    print(read_meme["image_url"])
    print(data["file"])
    assert read_meme["image_url"] == f"http://minio:9000/memes/{data['file'][1]}"


@pytest.mark.asyncio
async def test_delete_meme(client: TestClient, db_session: AsyncSession):

    async with AsyncClient(app=app, base_url="http://test", timeout=None) as ac:
        delete_response = await ac.delete(f"/memes/{created_meme_id}")

    assert delete_response.status_code == 200
    deleted_meme = delete_response.json()
    assert deleted_meme["id"] == created_meme_id
    assert deleted_meme["title"] == title
    assert deleted_meme["description"] == description

    async with AsyncClient(app=app, base_url="http://test", timeout=None) as ac:
        read_response = await ac.get(f"/memes/{created_meme_id}")

    assert read_response.status_code == 404
    assert read_response.json() == {"detail": "Meme not found"}
