from pydantic import BaseModel

class OtpCreate(BaseModel):
    phone: str
    code: int