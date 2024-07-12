import os


class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql+asyncpg://user:password@localhost/memes_db')
    S3_ENDPOINT_URL: str = os.getenv('S3_ENDPOINT_URL', 'http://localhost:9000')
    S3_ACCESS_KEY: str = os.getenv('S3_ACCESS_KEY', 'minioadmin')
    S3_SECRET_KEY: str = os.getenv('S3_SECRET_KEY', 'minioadmin')
    S3_BUCKET_NAME: str = os.getenv('S3_BUCKET_NAME', 'memes')


settings = Settings()
