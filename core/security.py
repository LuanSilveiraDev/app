from passlib.context import CryptContext


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