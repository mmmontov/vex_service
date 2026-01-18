from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class ApiV1Prefix(BaseModel):
    prefix: str = '/v1'
    marzban: str = '/marzban'
    blitz: str = '/blitz'
    

class ApiPrefix(BaseModel):
    v1: ApiV1Prefix = ApiV1Prefix()
    

class DatabaseConfig(BaseModel):
    url: str


class BlitzPanel(BaseModel):
    url: str
    username: str
    password: str
    

class Marzban(BaseModel):
    url: str
    username: str
    password: str

    
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env.template', '.env'),
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__',
    )
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    blitz: BlitzPanel
    marzban: Marzban
    
    
settings = Settings()

