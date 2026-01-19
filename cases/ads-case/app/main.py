import uvicorn
from fastapi import FastAPI
from app.routes import banner_tracker
from app.middlewares.fake_firewall_middleware import FakeFirewallMiddleware

app = FastAPI(title="Tracking Banner AD App")

app.include_router(banner_tracker.router, prefix="/banner")

app.add_middleware(FakeFirewallMiddleware)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8002,
        reload=False
    )