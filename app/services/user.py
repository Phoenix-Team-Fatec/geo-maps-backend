from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError
from repositories.user import create_user, find_user_by_email, get_all_users
from schemas.user import UserCreate
from core.security import get_password_hash, verify_password

#Erro caso os usuários já existam
class UserAlreadyExistsError(Exception):
    pass

#Erro caso as credenciais estejam erradas
class AuthError(Exception):
    pass

#Normaliza os emails para gravar no banco
def _normalize_email(email: str) -> str:
    return email.lower()

#Normaliza o cpf para gravar no banco
def _normalize_cpf(cpf: str | None) -> str | None:
    return "".join(filter(str.isdigit, cpf)) if cpf else None

#Cria usuário no banco de dados
async def create_user_service(user_data: UserCreate):
    data = user_data.model_dump(exclude_none=True)
    #Normaliza o email e o cpf
    data["email"] = _normalize_email(data["email"])
    data["cpf"] = _normalize_cpf(data.get("cpf"))
    #Transforma a senha em um hash
    plain = data.pop("password")
    hashed = get_password_hash(plain)
    #Adiciona a senha hash no json a ser enviado
    doc = jsonable_encoder({**data, "hashed_password": hashed})
    try:
        return await create_user(doc)
    except DuplicateKeyError as e:
        #Se já existir um usuário com o mesmo email ou cpf, cai aqui
        raise UserAlreadyExistsError("Email ou CPF já cadastrado.") from e

#Autentica o usuário no login
async def authenticate_user(email: str, password: str) -> dict:
    #Normaliza o email e busca o usuário no banco
    email = _normalize_email(email)
    user = await find_user_by_email(email)
    #Verifica se o usuário existe e se a senha bate
    user_is_blocked = user.get("is_blocked", False) if user else False
    if not user or not verify_password(password, user.get("hashed_password", "")):
        raise AuthError("Credenciais inválidas")
    if user_is_blocked:
        raise AuthError("Usuário bloqueado")
    return user


async def get_all_users_service() -> list[dict]:
    users = await get_all_users()
    return [user.model_dump(exclude={"hashed_password"}) for user in users]