from typing import Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt
from jwt.exceptions import DecodeError
from auth.models import User

from base.database import SessionLocal, get_db
from auth.crud import get_user_or_false

from base import settings
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
            payload = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=settings.ALGORITHM
            )

            if payload.get('pk', False):
                if get_user_or_false(db=self.db, user_id=payload['pk']):
                    valid = True

        except DecodeError:
            valid = False

        return valid


def authenticate(
    request: Request,
    token: str = Depends(JWTAuthentication()),
    db: Session = Depends(get_db)
) -> Optional[User]:

    payload = jwt.decode(
        jwt=token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM
    )

    if payload.get('pk', False):
        user = get_user_or_false(db=db, user_id=payload['pk'])

        if settings.EMAIL_VERIFICATION_IS_NEEDED:
            if not user.email_verified:
                raise HTTPException(
                    status_code=403,
                    detail="Please verify your email"
                )

        if user:
            return user
        else:
            raise HTTPException(status_code=403, detail="Not authenticated")


def authenticate_via_websockets(
    token: str,
    db: Session = Depends(get_db),
) -> Optional[User]:

    payload = jwt.decode(
        jwt=token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM
    )

    print(payload.get('pk', False))

    if payload.get('pk', False):
        return get_user_or_false(db=db, user_id=payload['pk'])
