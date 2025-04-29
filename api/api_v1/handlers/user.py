from fastapi import APIRouter, HTTPException, status
import pymongo.errors
from schemas.user_schema import UserAuth, UserDetail
from services.user_service import UserService
import pymongo

user_router = APIRouter()


@user_router.post('/adiciona', summary='Adiciona Usuário', response_model=UserDetail)
async def adiciona_usuario(data: UserAuth):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username ou e-mail deste usuário já existe'
        )
    #         # Analisa a mensagem de erro para determinar qual campo causou a duplicação
    #     error_msg = str(e)
    #     if 'email' in error_msg:
    #         detail = 'Este e-mail já está cadastrado'
    #     elif 'username' in error_msg:
    #         detail = 'Este nome de usuário já está em uso'
    #     else:
    #         detail = 'Username ou e-mail deste usuário já existe'

    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=detail
    #     )
    # except Exception as e:
    #     # Captura outros erros inesperados
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f'Ocorreu um erro ao criar o usuário: {str(e)}'
    #     )