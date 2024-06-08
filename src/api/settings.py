from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int = 5555
    host: str = 'localhost'
    max_file_size: int = 1024 * 1024 * 5
