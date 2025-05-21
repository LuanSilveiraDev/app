from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional

class User(Document):
    """
    Modelo de usuário para persistência em banco de dados MongoDB usando Beanie.

    Esta classe representa um usuário do sistema, incluindo informações de identificação,
    autenticação e status. Também fornece métodos utilitários para manipulação e consulta de usuários.

    Atributos:
        user_id (UUID): Identificador único do usuário. Gerado automaticamente com `uuid4`.
        username (str): Nome de usuário único e indexado.
        email (EmailStr): E-mail único e indexado do usuário.
        hash_password (str): Senha criptografada do usuário.
        first_name (Optional[str]): Primeiro nome do usuário (opcional).
        last_name (Optional[str]): Sobrenome do usuário (opcional).
        disabled (Optional[str]): Indica se o usuário está desativado (pode representar um status ou flag).
    """
    user_id: UUID = Field(default_factory=uuid4)
    username: str = Indexed(unique=True)
    email:  EmailStr = Indexed(unique=True) 
    hash_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[str] = None
    
    def __repr__(self) -> str:
        """
        Representação informal do objeto, útil para debug/logging.

        Retorna:
            str: Representação com o e-mail do usuário.
        """
        return f'User {self.email}'
    
    def __str__(self) -> str:
        """
        Representação como string simples do usuário.

        Retorna:
            str: E-mail do usuário.
        """
        return self.email

    def __eq__(self, other: object) -> bool:
        """
        Compara dois objetos User pela igualdade de e-mail.

        Parâmetros:
            other (object): Outro objeto a ser comparado.

        Retorna:
            bool: True se os e-mails forem iguais e o objeto for uma instância de User.
        """
        if isinstance(other, User):
            return self.email == other.email
        return False
    
    @property
    def create(self) -> datetime:   
        """
        Retorna a data e hora de criação do documento no MongoDB,
        com base no timestamp embutido no ObjectId (`self.id`).

        Retorna:
            datetime: Data de criação do documento.
        """
        return self.id.generation_time

    @classmethod
    async def by_email(self, email: str) -> "User":
        """
        Recupera um usuário do banco de dados com base no e-mail.

        Parâmetros:
            email (str): E-mail do usuário a ser buscado.

        Retorna:
            User: Objeto do tipo User correspondente, ou None se não encontrado.
        """
        return await self.find_one(self.email == email)