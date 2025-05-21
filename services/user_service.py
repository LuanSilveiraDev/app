from models.user_model import User
from schemas.user_schema import UserAuth
from core.security import get_password, verify_password
from typing import Optional
from uuid import UUID

class UserService:
    """
    Serviço de manipulação de usuários, responsável por operações como criação de usuário.
    """
    @staticmethod
    async def create_user(user: UserAuth):
        """
        Cria um novo usuário no sistema.
        
        Parâmetros: 
            user (UserAuth): Objeto que contém os dados de autorização do usuário (username, email, password)
                - username (str): Nome de usuário do novo usuário
                - email (str): E-mail do novo usuário
                - password (str): Senha do novo usuário
            Retorna:
                User: Objeto do tipo 'user' que representa o usuário recém-criado, com a senha criptografada
            
            Processos:
                1. Cria um novo objeto 'User' com as informações fornecidas
                2. Criptografa a senha do usuário usando a função 'get_passowrd'
                3. Salva o usuário no banco de dados de forma assincrona
                4. Retorna o objeto 'User' recém-criado
                
            Exemplo:
                user_data = UserAuth(username="johndoe", email="john@example.com", password="password123")
                new_user = await UserService.create_user(user_data)
        """

        usuario = User (
            username = user.username,
            email = user.email,
            hash_password = get_password(user.password)
        )
        
        await usuario.save()
        return usuario
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """
    Recupera um usuário do banco de dados com base no endereço de e-mail fornecido.

    Args:
        email (str): O endereço de e-mail do usuário a ser buscado.

    Returns:
        Optional[User]: O objeto `User` correspondente ao e-mail, se encontrado; caso contrário, `None`.
    """ 
        user = await User.find_one(User.email == email)
        return user
    
    
    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == id)
        return user
    
    
    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        """
    Autentica um usuário com base no e-mail e na senha fornecidos.

    Args:
        email (str): O endereço de e-mail do usuário.
        password (str): A senha em texto plano fornecida pelo usuário.

    Returns:
        Optional[User]: O objeto `User` autenticado se as credenciais forem válidas; caso contrário, `None`.
        """
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(
            password=password,
            hashed_password=user.hash_password
        ):
            return None
        return user