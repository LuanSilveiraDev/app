from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserAuth(BaseModel):
    """
    Schema de dados para autenticação e criação de usuários.

    Esta classe define os campos necessários para criar um novo usuário ou autenticar um usuário existente.
    Utiliza validações automáticas oferecidas pelo Pydantic.

    Atributos:
        email (EmailStr): Endereço de e-mail válido do usuário.
        username (str): Nome de usuário com no mínimo 5 e no máximo 50 caracteres.
        password (str): Senha do usuário com no mínimo 5 e no máximo 20 caracteres.
    """
    email: EmailStr = Field(..., description='E-mail do Usuário')
    username: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description='Username'
    )
    password: str = Field(
        ...,
        min_length=5,
        max_length=20,
        description='Senha do Usuário'
    )
    
class UserDetail(BaseModel):
    user_id: UUID
    username: str
    email: str