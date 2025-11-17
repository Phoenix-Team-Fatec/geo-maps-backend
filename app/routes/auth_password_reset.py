# routes/auth_password_reset.py (ou dentro do seu arquivo atual)
from fastapi import APIRouter, BackgroundTasks, Response, status
from app.schemas.auth_password_reset import ForgotPasswordIn, VerifyResetCodeIn, ResetPasswordIn
from app.services.password_reset import start_password_reset, verify_reset_code, reset_password
from app.utils.email_utils import send_reset_email

auth = APIRouter(prefix="/auth", tags=["Password Reset"])

@auth.post("/password/forgot", status_code=status.HTTP_204_NO_CONTENT)
async def forgot_password(payload: ForgotPasswordIn, background: BackgroundTasks):
    code = await start_password_reset(payload.email)
    if code:
        send_reset_email(payload.email, code, background=background)
    return Response(status_code=204)

@auth.post("/password/verify", status_code=status.HTTP_204_NO_CONTENT)
async def verify_code(payload: VerifyResetCodeIn):
    await verify_reset_code(payload.email, payload.code)
    return Response(status_code=204)

@auth.post("/password/reset", status_code=status.HTTP_204_NO_CONTENT)
async def do_reset(payload: ResetPasswordIn):
    await reset_password(payload.email, payload.code, payload.new_password)
    return Response(status_code=204)