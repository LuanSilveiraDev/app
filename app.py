# Importações principais do FastAPI e configuração do projeto
from fastapi import FastAPI
from core.config import settings

#Importações do Beanie e do Motor para integração com MongoDB
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

# Importações de modelos e rotas
from models.user_model import User
from api.api_v1.router import router
from models.task_model import Task

from fastapi.middleware.cors import CORSMiddleware
# Criação da instância principal do FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME, # Nome do projeto (definido em settings)
    openapi_url=f'{settings.API_V1_STR}/openapi.json' # Caminho personalizado para documentação OpenAPI
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
# Evento que será executado automaticamente no inicio da aplicação
@app.on_event("startup")
async def app_init():
    """
    Inicializa a conexão com o MongoDB e seleciona o banco 'todoapp'
    """
    # Cria cliente de conexão com o MongoDB e seleciona o banco 'todoapp'
    cliente_db = AsyncIOMotorClient(
        settings.MONGO_CONNECTION_STRING).todoapp

    # Inicializa o Beanie, associando o banco de dados e os modelos de documentos
    await init_beanie(
        database = cliente_db,
        document_models = [
            User, # Adiciona o modelo User para ser gerenciado pelo Beanie
            Task
        ]
    )

# Inclusão das rotas da API, com o prefixo definido nas configurações
app.include_router(
    router,
    prefix=settings.API_V1_STR
)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)