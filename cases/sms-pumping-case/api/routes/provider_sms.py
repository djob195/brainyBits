from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/billing")
def get_billing(request: Request):
    
    sms_provider = request.app.state.sms_provider

    return sms_provider.print_my_billing()