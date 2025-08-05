# from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     path: str
#     database_username: str = "postgres"
#     secret_key : str = "skdjafhklbs"
    
# settings = Settings()   # type: ignore

# print(settings.path)


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = "localhost"      #case insensitive for pydantic
    database_port: str
    database_name: str
    database_password: str
    database_username: str = "postgres"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
    
settings = Settings()   # type: ignore



