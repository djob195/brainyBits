import random
from collections import defaultdict

class FakeFirewallMiddleware:
    def __init__(self, app):
        self.app = app

        self.countries = ["US", "MX", "AR", "CL", "CO"]

        self.total_requests = 0
        self.requests_by_country = defaultdict(int)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            fake_ip = self._generate_fake_ip()
            country = random.choice(self.countries)

            self.total_requests += 1
            self.requests_by_country[country] += 1

            headers = list(scope.get("headers", []))
            headers.append((b"x-forwarded-for", fake_ip.encode()))
            headers.append((b"x-country", country.encode()))
            scope["headers"] = headers

            scope.setdefault("state", {})
            scope["state"]["firewall_ip"] = fake_ip
            scope["state"]["country"] = country
            scope["state"]["firewall_metrics"] = {
                "total_requests": self.total_requests,
                "requests_by_country": dict(self.requests_by_country)
            }

        await self.app(scope, receive, send)

    def _generate_fake_ip(self) -> str:
        return ".".join(str(random.randint(1, 254)) for _ in range(4))