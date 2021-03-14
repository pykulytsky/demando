import typing
from fastapi.testclient import TestClient
import requests
from sqlalchemy.orm import Session
from starlette.testclient import (
    ASGI2App, ASGI3App, Cookies, DataType, FileType, Params, TimeOut)

from auth import schemas
from auth import crud


class BearerAuth(requests.auth.AuthBase):
    """Base Bearer authentication"""

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["authorization"] = "Bearer " + self.token
        return request


class JWTAuthTestClient(TestClient):
    def __init__(
            self,
            app: typing.Union[ASGI2App, ASGI3App],
            user: schemas.User,
            base_url: str,
            db: Session,
            raise_server_exceptions: bool,
            root_path: str) -> None:

        self.db = db
        self.user = crud.get_user(self.db, user.id)

        super().__init__(
            app,
            base_url=base_url,
            raise_server_exceptions=raise_server_exceptions,
            root_path=root_path)

    def request(
        self,
        method: str,
        url: str,
        params: Params,
        data: DataType,
        headers: typing.MutableMapping[str, str],
        cookies: Cookies,
        files: FileType,
        timeout: TimeOut,
        allow_redirects: bool,
        proxies: typing.MutableMapping[str, str],
        hooks: typing.Any,
        stream: bool,
        verify: typing.Union[bool, str],
        cert: typing.Union[str, typing.Tuple[str, str]],
        json: typing.Any
    ) -> requests.Response:

        return super().request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=BearerAuth(self.user.token),
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json
        )
