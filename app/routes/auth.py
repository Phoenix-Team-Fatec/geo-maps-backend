from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.user import UserCreate, UserRead, Token, Credentials
from app.services.user import create_user_service, authenticate_user, UserAlreadyExistsError, AuthError
from app.core.security import create_access_token, create_refresh_token, decode_token, refresh_session, revoke_jti, ALGORITHM, SECRET_KEY
from app.repositories.user import find_user_by_email

#Declara o prefixo das rotas de autenticação, e a forma de receber o token
auth = APIRouter(prefix="/auth", tags=["Auth"])
bearer_scheme = HTTPBearer(auto_error=False)

#Declara as constantes dos cookies
REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_MAX_AGE = 365 * 24 * 60 * 60
COOKIE_SAMESITE = "lax"
COOKIE_SECURE = True 

#Função para extrair o token Bearer do header Authorization
def get_bearer_token(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Bearer token ausente")
    return creds.credentials

#Rota para registrar um novo usuário
@auth.post('/register', response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate):
    try:  
         return await create_user_service(payload)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#Rota para login e emissão dos tokens
@auth.post("/login", response_model=Token)
async def login(creds: Credentials, response: Response):
    try:
        user = await authenticate_user(creds.email, creds.password)
        access = create_access_token(subject=str(user["_id"]), extra={"email": user["email"]})
        refresh = create_refresh_token(subject=str(user["_id"]))
        response.set_cookie(
            key=REFRESH_COOKIE_NAME,
            value=refresh,
            httponly=True,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=REFRESH_COOKIE_MAX_AGE,
            path="/auth",
        )
        return {"access_token": access, "expires_in": 15 * 60, "token_type": "bearer"}
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))

#Rota para refresh do access token usando o refresh token do cookie
@auth.post("/refresh", response_model=Token)
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token ausente")

    try:
        new_access, new_refresh = refresh_session(refresh_token)

        response.set_cookie(
            key=REFRESH_COOKIE_NAME,
            value=new_refresh,
            httponly=True,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            max_age=REFRESH_COOKIE_MAX_AGE,
            path="/auth",
        )

        return {"access_token": new_access, "refresh_token": new_refresh, "expires_in": 15 * 60, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

#Rota para logout, revoga o refresh token 
@auth.post("/logout", status_code=204)
async def logout(request: Request, response: Response):
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if refresh_token:
        try:
            payload = decode_token(refresh_token)
            jti = payload.get("jti")
            if jti:
                revoke_jti(jti)
        except JWTError:
            pass
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/auth")
    return Response(status_code=204)

#Rota para obter os dados do usuário logado
@auth.get("/me", response_model=UserRead)
async def me(token: str = Depends(get_bearer_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if not email:
            raise HTTPException(401, "Token inválido")
        user = await find_user_by_email(email)
        if not user:
            raise HTTPException(401, "Usuário não encontrado")
        return UserRead(
            id=str(user["_id"]),
            cpf=user.get("cpf"),
            nome=user.get("nome"),
            sobrenome=user.get("sobrenome"),
            data_nascimento=user.get("data_nascimento"),
            email=user["email"],
            image=user.get("image"),
        )
    except JWTError:
        raise HTTPException(401, "Token inválido ou expirado")