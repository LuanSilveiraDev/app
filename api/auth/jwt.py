from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from services.user_service import UserService
from core.security import create_access_token, create_refresh_token
from schemas.auth_schema import TokenSchema
from schemas.user_schema import UserDetail
from models.user_model import User
from api.dependencies.user_deps import get_current_user

auth_router = APIRouter()

@auth_router.post('/login', summary='Cria Access Token e Refresh Token', response_model=TokenSchema)
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Endpoint para autenticação de usuários.

    Recebe credenciais via formulário OAuth2 (usuário e senha) e,
    se autenticado com sucesso, retorna um token de acesso (access token)
    e um token de atualização (refresh token).

    Args:
        data (OAuth2PasswordRequestForm, optional): Dependência do FastAPI que extrai os dados do formulário
            (username e password).

    Returns:
        dict: Um dicionário contendo:
            - "access_token": Token JWT para autenticação nas rotas protegidas.
            - "refresh_token": Token JWT para obtenção de um novo access token.

    Raises:
        HTTPException: Se o e-mail ou a senha estiverem incorretos, retorna status 400 (Bad Request).
    """
    usuario = await UserService.authenticate(
        email = data.username,
        password = data.password
    )
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ou senha estão incorretos"
        )
    
    return {
        "access_token": create_access_token(usuario.user_id),
        "refresh_token": create_refresh_token(usuario.user_id)
    }
    
@auth_router.post('/test-token', summary='Testanto Token',   response_model=UserDetail)
async def test_token(user: User = Depends(get_current_user)):
    return user