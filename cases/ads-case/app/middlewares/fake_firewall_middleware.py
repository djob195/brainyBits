import random
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class FakeFirewallMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.countries = ["US", "MX", "AR", "CL", "CO"]

    async def dispatch(self, request: Request, call_next):
        fake_ip = self._generate_fake_ip()
        country = random.choice(self.countries)

        request.scope["headers"].append(
            (b"x-forwarded-for", fake_ip.encode())
        )
        request.scope["headers"].append(
            (b"x-country", country.encode())
        )

        request.state.firewall_ip = fake_ip
        request.state.country = country

        return await call_next(request)

    def _generate_fake_ip(self) -> str:
        return ".".join(str(random.randint(1, 254)) for _ in range(4))
