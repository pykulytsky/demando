import httpx
from httpx import Request, Response
from httpx._config import (
    Limits,
    DEFAULT_TIMEOUT_CONFIG,
    DEFAULT_LIMITS,
    DEFAULT_MAX_REDIRECTS,
    UnsetType,
    UNSET
)
from httpx._types import (
    URLTypes,
    VerifyTypes,
    CertTypes,
    ProxiesTypes,
    QueryParamTypes,
    HeaderTypes,
    AuthTypes,
    CookieTypes,
    TimeoutTypes,
    RequestContent,
    RequestData,
    RequestFiles,
)
import httpcore

import typing
from ... import settings

from urllib.parse import urljoin


class BearerAuth(httpx.Auth):
    def __init__(self, token: str) -> None:
        self._auth_header = self._build_auth_header(token)

    def auth_flow(self, request: Request) -> typing.AsyncGenerator[Request, Response]:
        request['Authorization'] = self._auth_header

        yield request

    def _build_auth_header(token: str) -> str:
        return "Bearer " + token


class SendgridHTTP(httpx.AsyncClient):
    def __init__(
        self,
        *,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        verify: VerifyTypes = True,
        cert: CertTypes = None,
        http2: bool = False,
        proxies: ProxiesTypes = None,
        mounts: typing.Mapping[str, httpcore.AsyncHTTPTransport] = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        limits: Limits = DEFAULT_LIMITS,
        pool_limits: Limits = None,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: typing.Mapping[str, typing.List[typing.Callable]] = None,
        transport: httpcore.AsyncHTTPTransport = None,
        app: typing.Callable = None,
        trust_env: bool = True,
    ):
        auth = BearerAuth(token=settings.SENDGRID_API_KEY)
        base_url = settings.SENDGRID_BASE_URL

        super().__init__(
            auth=auth,
            params=params,
            headers=headers,
            cookies=cookies,
            verify=verify,
            cert=cert,
            http2=http2,
            proxies=proxies,
            mounts=mounts,
            timeout=timeout,
            limits=limits,
            pool_limits=pool_limits,
            max_redirects=max_redirects,
            event_hooks=event_hooks,
            base_url=base_url,
            transport=transport,
            app=app,
            trust_env=trust_env
        )

    async def request(
        self,
        method: str,
        url: URLTypes,
        *,
        content: RequestContent = None,
        data: RequestData = None,
        files: RequestFiles = None,
        json: typing.Any = None,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        auth: typing.Union[AuthTypes, UnsetType] = UNSET,
        allow_redirects: bool = True,
        timeout: typing.Union[TimeoutTypes, UnsetType] = UNSET,
    ) -> Response:

        url = self._format_url(url)

        return super().request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=allow_redirects,
            timeout=timeout
        )

    def _format_url(self, url: str):
        return urljoin(self.base_url, url.lstrip('/'))