from repositories.admin_repositorie import block_user, auth_admin

async def block_user_service(user_cpf: str, is_blocked: bool = False):
    return await block_user(user_cpf, is_blocked)

async def authenticate_admin(username: str, password: str) -> bool:
    return await auth_admin(username, password)

