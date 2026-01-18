from pydantic import BaseModel, Field
from typing import List, Optional


class UserInfo(BaseModel):
    username: str
    expiration_days: int
    remaining_days: int
    account_creation_date: str
    status: str
    upload_bytes: int
    download_bytes: int
    online_count: int
    ipv4: str
    

class CreateUser(BaseModel):
    username: str = Field(None)
    expiration_days: int = Field(30, description='Время на которое выдаётся подписка')
    traffic_limit: int = Field(0, description='ограничение трафика')
    note: str = Field('telegram', description='можно использовать для сохранения telegram-username пользователя')
    
    
class ApiResponse(BaseModel):
    detail: str