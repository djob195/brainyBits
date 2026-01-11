from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/firewall")
def firewall_metrics(request: Request):
    return request.state.firewall_metrics