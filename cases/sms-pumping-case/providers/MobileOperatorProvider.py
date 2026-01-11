import uuid

class FakeMobileOperatorProvider:
    def __init__(
        self,
        operator_name: str = "FakeMobileOperator",
        cost_per_sms: float = 0.001,
        currency: str = "USD"
    ):
        self.operator_name = operator_name
        self.cost_per_sms = cost_per_sms
        self.currency = currency

        self.total_spent = 0.0
        self.messages_processed = 0
        self.messages_approved = 0
        self.messages_rejected = 0

    def approve_sms(self, phone: str, message: str) -> dict:

        self.messages_processed += 1

        self.messages_approved += 1
        self.total_spent += self.cost_per_sms
        return {
            "operator": self.operator_name,
            "approved": True,
            "operator_message_id": str(uuid.uuid4()),
            "billing": {
                "cost": self.cost_per_sms,
                "currency": self.currency,
                "total_spent": round(self.total_spent, 2),
                "messages_processed": self.messages_processed,
                "approved": self.messages_approved,
                "rejected": self.messages_rejected
            }
        }

    def get_billing_summary(self) -> dict:
        return {
            "operator": self.operator_name,
            "messages_processed": self.messages_processed,
            "approved": self.messages_approved,
            "rejected": self.messages_rejected,
            "cost_per_sms": self.cost_per_sms,
            "total_spent": round(self.total_spent, 2),
            "currency": self.currency
        }


