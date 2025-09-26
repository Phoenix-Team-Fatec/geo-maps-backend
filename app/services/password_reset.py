# services/password_reset.py
from bson import ObjectId
from fastapi import HTTPException, status
from typing import Optional
from repositories.user import find_user_by_email
from repositories.reset_tokens import (
    create_reset_token, get_active_token, increment_attempts, mark_used
)
from core.security import get_password_hash, generate_code, hash_code, verify_code, expires_at_from_now, MAX_RESET_ATTEMPTS
from core.database import users_collection

def _normalize_email(email: str) -> str:
    return email.lower()

async def start_password_reset(email: str) -> Optional[str]:
    email = _normalize_email(email)
    user = await find_user_by_email(email)
    # Sempre retorna 204 para evitar enumeração de e-mails
    if not user:
        return
    # Reaproveita token ativo, se houver, ou gera novo

    code = generate_code()
    code_h = hash_code(code)
    await create_reset_token(user["_id"], code_h, expires_at_from_now())
    # Retorna o code para quem for enviar por e-mail no controller (ou pode enviar aqui)
    return code  # opcionalmente retornar para camada de rota enviar e-mail

async def verify_reset_code(email: str, code: str) -> None:
    email = _normalize_email(email)
    user = await find_user_by_email(email)
    # Não revelar existência
    if not user:
        return
    token = await get_active_token(user["_id"])
    if not token:
        raise HTTPException(status_code=400, detail="Código inválido ou expirado")
    if token["attempts"] >= MAX_RESET_ATTEMPTS:
        raise HTTPException(status_code=429, detail="Muitas tentativas. Solicite um novo código.")
    if not verify_code(code, token["code_hash"]):
        await increment_attempts(token["_id"])
        raise HTTPException(status_code=400, detail="Código inválido")
    # Se chegou aqui, está ok (não marca como usado ainda)

async def reset_password(email: str, code: str, new_password: str) -> None:
    email = _normalize_email(email)
    user = await find_user_by_email(email)
    # Mesmo comportamento para não revelar
    if not user:
        return
    token = await get_active_token(user["_id"])
    if not token:
        raise HTTPException(status_code=400, detail="Código inválido ou expirado")
    if token["attempts"] >= MAX_RESET_ATTEMPTS:
        raise HTTPException(status_code=429, detail="Muitas tentativas. Solicite um novo código.")
    if not verify_code(code, token["code_hash"]):
        await increment_attempts(token["_id"])
        raise HTTPException(status_code=400, detail="Código inválido")

    # Troca a senha
    hashed = get_password_hash(new_password)
    await users_collection.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": {"hashed_password": hashed}}
    )
    await mark_used(token["_id"])
