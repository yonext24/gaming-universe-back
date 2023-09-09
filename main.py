from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from dotenv import load_dotenv

from db.dbconfig import engine
from routers import auth_router, categories_router, products_router

from db import models


load_dotenv()
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Fast API PCS Ecommerce",
    description="API to manage ecommerce made with NextJS and Typescript.",
    version="0.0.1",
    contact={
        "name": "Jonathan",
        "email": "yonielkpo@gmail.com",
    },
)


class AuthenticationHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        bool = "true"

        try:
            if not response.headers.get("set-cookie"):
                request.cookies["session_id"]
        except KeyError:
            print("KeyError")
            bool = "false"

        response.headers["X-Authenticated"] = bool

        return response


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
    ],
)
app.add_middleware(AuthenticationHeaderMiddleware)

app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(categories_router.router)
