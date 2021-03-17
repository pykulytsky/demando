from typing import Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt
from jwt.exceptions import DecodeError
from auth.models import User

from base.database import SessionLocal
from auth.crud import get_user_or_false

from base import settings
from tests.test_database import TestSessionLocal


class JWTAuthentication(HTTPBearer):
    """Authentication using JWT tokens."""

    def __init__(self, auto_error: bool = True):
        self.db = SessionLocal()
        super(JWTAuthentication, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        try:
            if request['headers'][1][1] == b'testclient':
                self.db = TestSessionLocal()
        except TypeError:
            if request.__dict__['headers']['user-agent'] == 'testclient':
                self.db = TestSessionLocal()

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
                if get_user_or_false(db=self.db, user_id=paylaod['pk']):
                    valid = True

        except DecodeError:
            valid = False

        return valid


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate(
    request: Request, token: str = Depends(JWTAuthentication())
) -> Optional[User]:

    db = SessionLocal()

    try:
        if request['headers'][1][1] == b'testclient':
            db = TestSessionLocal()
    except TypeError:
        if request.__dict__['headers']['user-agent'] == 'testclient':
            db = TestSessionLocal()

    paylaod = jwt.decode(
        jwt=token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM
    )

    if paylaod.get('pk', False):
        user = get_user_or_false(db=db, user_id=paylaod['pk'])
        if user:
            return user
        else:
            raise HTTPException(status_code=403, detail="Not authenticated")
