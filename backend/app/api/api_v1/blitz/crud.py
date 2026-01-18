from aiohttp import ClientSession, ClientTimeout, TCPConnector, ClientError
from aiohttp.cookiejar import CookieJar

from core.config import settings
from .schemas import CreateUser, UserInfo
from utils.calculate_functions import count_remaining_days

class BlitzClient:
    def __init__(self):
        self.base_url = settings.blitz.url
        self.username = settings.blitz.username
        self.password = settings.blitz.password
        self.api_version_prefix = f'/api{settings.api.v1.prefix}'
        
        self.session: ClientSession | None = None
        self.logged_in: bool = False
        
        
    async def _get_session(self) -> ClientSession:
        if self.session is None or self.session.closed:
            self.session = ClientSession(
                cookie_jar=CookieJar(unsafe=True),  # кукесы
                timeout=ClientTimeout(total=20),
                connector=TCPConnector(ssl=False),  # чтобы работало даже если сайт "небезопасный"
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    )
                }, # без хедеров не пускает 
            )
        return self.session


    async def login(self):
        session = await self._get_session()
        
        response = await session.post(
            f'{self.base_url}/login',
            data={
                'username': self.username,
                'password': self.password
            },
            allow_redirects=True
        )
        
        if response.status not in (200, 302):
            raise Exception("Blitz login failed")
        
        self.logged_in = True


    async def _request(self, method: str, path: str, **kwargs):
        session = await self._get_session()
        
        if not self.logged_in:
            await self.login()
        
        for _ in range(2):
            try:
                response = await session.request(
                    method,
                    f"{self.base_url}{path}",
                    allow_redirects=True,
                    **kwargs,
                    
                )
                return response
            
            except ClientError:
                self.logged_in = False
                await self.login()
                
        raise RuntimeError("Blitz request failed after retry")
            
    
    # получить информацию о сервере
    async def get_server_status(self):
        response = await self._request(
            "GET",
            f"{self.api_version_prefix}/server/status"
        )
        
        return await response.json()
    
    
    # получить информацию о пользователе
    async def get_user_info(self, username: str | int) -> UserInfo:
        response = await self._request(
            'GET',
            f'{self.api_version_prefix}/users/{username}'
        )
        
        response_subscribe = await self._request(
            'GET',
            f'{self.api_version_prefix}/users/{username}/uri'
        )
        
        sub_data = await response_subscribe.json()
        data = await response.json()
        date = data['account_creation_date']
        days = data['expiration_days']
        data['remaining_days'] = count_remaining_days(date, days)
        data['ipv4'] = sub_data['ipv4']
        data = UserInfo(**data)
        return data
    
    
    # создать пользователя
    async def create_user(self, data: CreateUser):
        response = await self._request(
            'POST',
            f'{self.api_version_prefix}/users',
            json=data.model_dump()
        )
        
        return await response.json()
        
        
    # обновление подписки пользователя
    async def reset_user(self, username: str | int):
        response = await self._request(
            'GET',
            f'{self.api_version_prefix}/users/{username}/reset'
        )
        return await response.json()
    
    # закрытие сессии подключения
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


blitz_client = BlitzClient()

