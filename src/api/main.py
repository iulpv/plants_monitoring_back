import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.root import router as root_router
from src.api.routes.predict import router as predict_router
from src.api.settings import Settings


def main():
    settings = Settings()
    api = FastAPI()
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["127.0.0.1:3000", "192.168.0.104:3000", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    api.include_router(root_router)
    api.include_router(predict_router)
    uvicorn.run(api, host=settings.host, port=settings.port)


if __name__ == '__main__':
    main()
