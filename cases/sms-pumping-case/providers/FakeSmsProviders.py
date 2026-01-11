import uuid
from providers.MobileOperatorProvider import FakeMobileOperatorProvider

class FakeSMSProvider:
    def __init__(
        self,
        provider_name: str = "FakeSMS",
        cost_per_sms: float = 0.005,
        currency: str = "USD"
    ):
        self.provider_name = provider_name
        self.cost_per_sms = cost_per_sms
        self.currency = currency

        # Billing state
        self.total_spent = 0.0
        self.messages_sent = 0
        self.mobile_provider = FakeMobileOperatorProvider()

    def send_sms(self, phone: str, message: str) -> dict:

        message_id = str(uuid.uuid4())

        json_mobile = self.mobile_provider.approve_sms(phone, message)

        if not json_mobile["approved"]:
            return {"success": False,
            "provider": self.provider_name,
            "message_id": message_id}

        self.messages_sent += 1
        self.total_spent += self.cost_per_sms

        return {
            "success": True,
            "provider": self.provider_name,
            "message_id": message_id,
            "billing": {
                "cost": self.cost_per_sms,
                "currency": self.currency,
                "total_spent": round(self.total_spent, 2),
                "messages_sent": self.messages_sent
            }
        }

    def print_billing_customer(self):
       return {
            "provider": self.provider_name,
            "messages_sent": self.messages_sent,
            "total_spent": round(self.total_spent, 2),
            "currency": self.currency,
            "cost_per_sms": self.cost_per_sms
        }
    
    def print_my_billing(self):
       return self.mobile_provider.get_billing_summary()
