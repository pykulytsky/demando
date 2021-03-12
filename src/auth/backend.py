from typing import Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt
from jwt.exceptions import DecodeError

from base.database import SessionLocal
from auth.crud import get_user_or_false

from base import settings


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class JWTAuthentication(HTTPBearer):
    """Authentication using JWT tokens."""

    def __init__(self, auto_error: bool = True):
        self.db = SessionLocal()
        super(JWTAuthentication, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials: HTTPAuthorizationCredentials = await super(
            JWTAuthentication, self
        ).__call__(request)

        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme."
                )
            if await self._verify__jwt_token(credentials.credentials):
                return credentials.credentials
            else:
                raise HTTPException(status_code=403, detail="Token not valid")
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid authorization code."
            )

    async def _verify__jwt_token(self, token: str) -> bool:
        valid: bool = False

        try:
            paylaod = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=settings.ALGORITHM
            )

            if paylaod.get('id', False):
                if get_user_or_false(db=self.db, user_id=paylaod['id']):
                    valid = True

        except DecodeError:
            valid = False

        return valid
