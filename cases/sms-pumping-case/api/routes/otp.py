from fastapi import APIRouter, Request
from schemas.otp import OtpCreate

router = APIRouter()

@router.post("/")
def create_otp(request: Request, item: OtpCreate):
    
    sms_provider = request.app.state.sms_provider

    result = sms_provider.send_sms(
        phone=f"+{item.code}{item.phone}",
        message="1234"
    )


    return result


@router.get("/billing")
def get_billing(request: Request):
    
    sms_provider = request.app.state.sms_provider
    return sms_provider.print_billing_customer()