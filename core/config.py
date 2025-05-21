from typing import List
from decouple import config
from pydantic.v1 import AnyHttpUrl, BaseSettings

class Settings(BaseSettings):
    """
    Classe de configuração global da aplicação, utilizando Pydantic para validação e gerenciamento
    de variáveis de ambiente de forma segura e tipada.

    Atributos:
        API_V1_STR (str): Prefixo base para as rotas da API (ex: "/api/v1").
        JWT_SECRET_KEY (str): Chave secreta usada para assinar tokens JWT de acesso.
        JWT_REFRESH_SECRET_KEY (str): Chave usada para assinar tokens JWT de *refresh*.
        ALGORITHM (str): Algoritmo utilizado na geração/validação de tokens JWT (ex: HS256).
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Tempo de expiração do token de acesso em minutos (padrão: 60).
        REFRESH_TOKEN_EXPIRE_MINUTES (int): Tempo de expiração do token de *refresh* (padrão: 7 dias).
        BACKEND_CORS_ORIGINS (List[AnyHttpUrl]): Lista de origens permitidas para CORS (URLs confiáveis).
        PROJECT_NAME (str): Nome do projeto ou sistema.
        MONGO_CONNECTION_STRING (str): String de conexão com o banco de dados MongoDB.

    Config interna:
        case_sensitive (bool): Se as variáveis de ambiente devem ser sensíveis a maiúsculas/minúsculas.
    """
    API_V1_STR: str = '/api/v1'
    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY', cast=str)
    JWT_REFRESH_SECRET_KEY: str = config('JWT_REFRESH_SECRET_KEY', cast=str)
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 dias
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
         'http://localhost:3000',
         'http://127.0.0.1:5500'
    ]
    PROJECT_NAME: str = "TODOFast"
    
    # Database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    
    class Config:
        case_sensitive = True  # Diferencia maiúsculas de minúsculas nas variáveis de ambiente

# Instância global das configurações
settings = Settings()