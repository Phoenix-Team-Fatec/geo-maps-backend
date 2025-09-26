from pydantic import BaseModel, EmailStr, constr

class ForgotPasswordIn(BaseModel):
    email: EmailStr

class VerifyResetCodeIn(BaseModel):
    email: EmailStr
    code: constr(min_length=6, max_length=6)  # "123456"

class ResetPasswordIn(BaseModel):
    email: EmailStr
    code: constr(min_length=6, max_length=6)
    new_password: constr(min_length=8)
