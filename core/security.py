from passlib.context import CryptContext
from typing import Union, Any
from datetime import datetime, timedelta, timezone
from jose import jwt
from core.config import settings

# Contexto de criptografia utilizando o algoritmo bcrypt
password_context = CryptContext(
    schemes=["bcrypt"],  # Define os algoritmos suportados (bcrypt neste caso)
    deprecated="auto"    # Marca automaticamente algoritmos antigos como obsoletos
)
# Criptografia da senha 
def get_password(password: str) -> str:
    """
    Gera o hash de uma senha em texto plano utilizando o algoritmo bcrypt.

    Parâmetros:
        password (str): A senha em texto plano a ser criptografada.

    Retorna:
        str: A senha criptografada (hash).
    
    Exemplo:
        >>> get_password("minhaSenha123")
        '$2b$12$R4...'
    """
    return password_context.hash(password)

# Descriptografia da senha
def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.

    Parâmetros:
        password (str): Senha em texto plano inserida pelo usuário.
        hashed_password (str): Hash da senha armazenado no banco de dados.

    Retorna:
        bool: True se a senha for válida, False caso contrário.
    
    Exemplo:
        >>> verify_password("minhaSenha123", "$2b$12$R4...")
        True
    """
    return password_context.verify(password, hashed_password)

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Cria um token de acesso JWT assinado.

    Args:
        subject (Union[str, Any]): O assunto (subject) do token, normalmente o ID ou identificador do usuário.
        expires_delta (int, optional): Um intervalo de tempo (timedelta) personalizado para a expiração do token.
                                       Se não for fornecido, será usado o valor padrão definido em settings.

    Returns:
        str: O token JWT codificado como string.
    """
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    info_jwt = {
        "exp": expires_delta,
        "sub": str(subject)
    }
    
    jwt_encoded = jwt.encode(
        info_jwt,
        settings.JWT_SECRET_KEY,
        settings.ALGORITHM
    )
    
    return jwt_encoded

def create_refresh_token(subject: Union[str,Any], expires_delta: int = None) -> str:
    """
    Cria um token de atualização (refresh token) JWT assinado.

    Args:
        subject (Union[str, Any]): O assunto (subject) do token, geralmente o identificador do usuário.
        expires_delta (int, optional): Um intervalo de tempo (timedelta) personalizado para a expiração do token.
                                       Se não for fornecido, será usado o valor padrão definido em settings.

    Returns:
        str: O token de atualização JWT codificado como string.
    """
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    info_jwt = {
        "exp": expires_delta,
        "sub": str(subject)
    }
    
    jwt_encoded = jwt.encode(
        info_jwt,
        settings.JWT_REFRESH_SECRET_KEY,
        settings.ALGORITHM
    )   
    
    return jwt_encoded