from typing import Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt
from jwt.exceptions import DecodeError
from .models import User

from demando.base.database import SessionLocal, get_db
from .crud import get_user_or_false

from demando.base import settings
from sqlalchemy.orm import Session


class JWTAuthentication(HTTPBearer):
    """Authentication using JWT tokens."""

    def __init__(self, auto_error: bool = True):
        self.db = SessionLocal()
        super(JWTAuthentication, self).__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request, db: Session = Depends(get_db)
    ) -> Optional[str]:

        self.db = db

        credentials: HTTPAuthorizationCredentials = await super(
            JWTAuthentication, self
        ).__call__(request)

        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme."
                )
            if await self._verify_jwt_token(credentials.credentials):
                return credentials.credentials
            else:
                raise HTTPException(status_code=403, detail="Token not valid")
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid authorization code."
            )

    async def _verify_jwt_token(self, token: str) -> bool:
        valid: bool = False

        try:
            paylaod = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=settings.ALGORITHM
            )

            if paylaod.get('pk', False):
                if await User.get_or_404(paylaod['pk']):
                    valid = True

        except DecodeError:
            valid = False

        return valid


async def authenticate(
    request: Request,
    token: str = Depends(JWTAuthentication()),
    db: Session = Depends(get_db)
) -> Optional[User]:

    paylaod = jwt.decode(
        jwt=token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM
    )

    if paylaod.get('pk', False):
        user = await User.get_or_404(paylaod['pk'])
        if user:
            return user
        else:
            raise HTTPException(status_code=403, detail="Not authenticated")
