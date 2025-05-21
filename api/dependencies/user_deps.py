from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from models.user_model import User
from jose import jwt
from core.config import settings
from schemas.auth_schema import TokenPayload
from datetime import datetime
from pydantic import ValidationError
from services.user_service import UserService

# Cria um esquema OAuth2 para reutilização de tokens JWT.
# Esse esquema será usado em rotas protegidas para extrair o token do header Authorization (Bearer <token>).
oauth_reusavel = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/auth/login', # Endpoint onde o token é obtido (normalmente via POST)
    scheme_name='JWT'  # Nome descritivo do esquema, útil na documentação Swagger
)

# Função que tenta obter o usuário atual com base no token JWT fornecido.
# Ela será usada como dependência em rotas protegidas para validar e decodificar o token.
async def get_current_user(token: str = Depends(oauth_reusavel)) -> User:
    try:
        # Decodifica o token usando a chave secreta e o algoritmo definidos nas configurações
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY, # Chave secreta usada para assinar/verificar o JWT
            settings.ALGORITHM  # Algoritmo usado para assinar/verificar o JWT (ex: HS256)
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Erro na validação do token',
                headers={'WWW-Authenticate': 'Bearer'}
            )
         # Aqui você extrairia os dados relevantes do payload, como o ID do usuário,
        # e então faria uma consulta ao banco de dados para retornar o objeto User.
        # Exemplo (comentado pois depende da sua implementação):
        # user_id = payload.get("sub")
        # user = get_user_by_id(user_id)
        # if user is None:
        #     raise credentials_exception
        # return user
        
        # token data
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Erro na validação do Token",
            headers={'WWW-Authenticate': 'Bearer'}
        )
         # Em caso de erro (token inválido, expirado, etc.), você deveria lançar uma exceção apropriada.
        # Aqui está apenas passando sem tratamento, o que pode gerar problemas.
        # O ideal seria lançar um HTTPException com status 401.
    
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Não foi possivel encontrar o usuário',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    return user