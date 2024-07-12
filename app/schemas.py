from pydantic import BaseModel


class MemeBase(BaseModel):
    title: str
    description: str


class MemeCreate(MemeBase):
    pass


class MemeUpdate(MemeBase):
    pass


class Meme(MemeBase):
    id: int
    image_url: str

    class Config:
        orm_mode = True
