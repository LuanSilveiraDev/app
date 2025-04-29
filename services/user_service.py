from models.user_model import User
from schemas.user_schema import UserAuth
from core.security import get_password

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