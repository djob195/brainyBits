from fastapi import FastAPI
from api.routes.otp import router as otp_router
from providers.FakeSmsProviders import FakeSMSProvider
from api.routes.provider_sms import router as sms_router
from middleware.firewall import FakeFirewallMiddleware
from api.routes.metrics import router as metrics_router

sms_provider = FakeSMSProvider()

app = FastAPI(title="Auth service")

app.state.sms_provider = sms_provider
app.add_middleware(FakeFirewallMiddleware)


app.include_router(otp_router, prefix="/otp", tags=["Otp"])
app.include_router(sms_router, prefix="/sms-provider", tags=["SmsProvider"])
app.include_router(metrics_router, prefix="/metrics", tags=["Metrics"])
