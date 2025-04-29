from fastapi import APIRouter
from api.api_v1.handlers import user


# Cria uma instância do roteador principal da aplicação
router = APIRouter()

# Inclui as rotas relacionadas a usuários no roteador principal
router.include_router(
    user.user_router,  # Roteador definido no módulo de usuários
    prefix='/users',  # Prefixo comum para todas as rotas de usuário (ex: /users/login, /users/register)
    tags=['users']  # Tag utilizada na documentação automática (Swagger) para agrupar rotas de usuário
)

