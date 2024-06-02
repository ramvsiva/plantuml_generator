from fastapi.security import APIKeyHeader
from fastapi import Depends
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import os
from dotenv import load_dotenv
load_dotenv()

X_API_KEY = APIKeyHeader(name='X-API-Key')
API_KEY = os.getenv('X_API_KEY')


class HTTPHeaderAuthentication:
    def __init__(self):
        self.key = API_KEY

    async def __call__(self, request: Request, x_api_key: str = Depends(X_API_KEY)):
        if self.key != x_api_key:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=f"Provided authentication is invalid"
            )