from pydantic import BaseModel, HttpUrl, Field


class MemeBase(BaseModel):
    title: str = Field(..., max_length=100, min_length=1, description="Title")
    description: str = Field(..., max_length=300, description="Description")


class MemeCreate(MemeBase):
    image_url: HttpUrl = Field(..., description="URL of the image")


class MemeUpdate(MemeBase):
    title: str | None = None
    description: str | None = None
    image_url: HttpUrl | None = Field(None, description="URL of the image (optional)")

    class Config:
        orm_mode = True


class Meme(MemeBase):
    id: int
    image_url: str

    class Config:
        orm_mode = True
