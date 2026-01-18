from marzban import MarzbanAPI, UserCreate, ProxySettings, UserModify, UserResponse
import httpx

from core.config import settings
from utils.calculate_functions import calculate_sub_seconds
from .schemas import CreateUser

class MarzbanClient:
    def __init__(self):
        self.base_url = settings.marzban.url
        self.username = settings.marzban.username
        self.password = settings.marzban.password
        
        self.VLESS_PROXY = {"vless": ProxySettings(flow="xtls-rprx-vision")}
        self.VLESS_INBOUNDS = {'vless': ['VLESS TCP REALITY']}
        
        self.api = MarzbanAPI(base_url=self.base_url)
        
    # получение токена
    async def get_token(self):
        token = await self.api.get_token(
            username=self.username,
            password=self.password
        )
        return token.access_token
    
    
    # получить информацию о сервере
    async def get_server_status(self):
        token = await self.get_token()
        system_stats = await self.api.get_system_stats(token=token)
        return system_stats
    
    
    # получение информации о пользователе
    async def get_user_info(self, username: str) -> UserResponse:
        token = await self.get_token()
        
        try:
            user_info = await self.api.get_user(username=str(username), token=token)
            return user_info.model_dump_json()
        except httpx.HTTPStatusError as err:
            return {'status': err}
        
        
    # создание нового пользователя
    async def create_user(self, data: CreateUser) -> UserResponse:
        token = await self.get_token()
        
        user = UserCreate(
            **data.model_dump(),
            proxies=self.VLESS_PROXY,
            inbounds=self.VLESS_INBOUNDS,

        )
        try:
            added_user = await self.api.add_user(user=user, token=token)
            return added_user
        except httpx.HTTPStatusError as err:
            return {'status': err}
    
    
    async def reset_user(self, username: str, days: int = 30) -> UserResponse:
        token = await self.get_token()

        try:
            new_expire = calculate_sub_seconds(days)

            modified_user = await self.api.modify_user(username=str(username), 
                                            user=UserModify(expire=new_expire),
                                            token=token)
            return modified_user
        
        except Exception as err:
            return {'status': err}
            
        
            
marzban_client = MarzbanClient()