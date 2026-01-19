from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.mockups.image_url_mock import image_url_mock
from uuid import uuid4
from app.mockups.tracking_db_mock import tracking_db

router = APIRouter()

@router.get("/impression/{image_name}")
async def track_img(image_name: str, request: Request):
    allowed_extensions = (".png", ".jpg", ".jpeg", ".webp")

    if not image_name.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="File is not a valid image")
        
    ip = request.client.host
    country = getattr(request.state, "country", None)    
    uid = str(uuid4())

    image_url = image_url_mock.image_url(640, 480)

    tracking_db.register_impression(
        uid=uid,
        banner=image_name,
        ip=ip,
        country=country,
    )

    response = RedirectResponse(url=image_url, status_code=302)
    response.headers["X-Request-UID"] = uid  

    return response


@router.get("/click/{uid}")
async def track_click(uid: str, request: Request):
    if not uid:
        raise HTTPException(status_code=400, detail="UID Required")
    if not tracking_db.click_exists(uid):
        tracking_db.register_click(uid=uid, ip=request.client.host)
    return {"status": "click registered", "uid": uid}

@router.get("/stats")
async def get_stats():
    return tracking_db.stats()