from pydantic import BaseModel, Field
from typing import List, Optional


from utils.calculate_functions import calculate_sub_seconds

class CreateUser(BaseModel):
    username: str = Field(None)
    expire: int = Field(calculate_sub_seconds(days=30), description='Время на которое выдаётся подписка (по умолчанию 30 дней)')
    data_limit: int = Field(0, description='ограничение трафика')
    note: str = Field('telegram', description='можно использовать для сохранения telegram-username пользователя')
    