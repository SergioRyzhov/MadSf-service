from pydantic import BaseModel, HttpUrl, Field, ConfigDict


class MemeBase(BaseModel):
    title: str = Field(..., max_length=100, min_length=1, description="Title")
    description: str = Field(..., max_length=300, description="Description")


class MemeCreate(MemeBase):
    pass


class MemeUpdate(MemeBase):
    title: str | None = None
    description: str | None = None
    image_url: HttpUrl | None = Field(None, description="URL of the image (optional)")

    class Config:
        config_dict = ConfigDict(from_attributes=True)


class Meme(MemeBase):
    id: int
    image_url: str

    class Config:
        config_dict = ConfigDict(from_attributes=True)
