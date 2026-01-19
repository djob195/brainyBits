from datetime import datetime, timezone
from collections import defaultdict

class TrackingDBMock:
    def __init__(self):
        self.impressions = {}
        self.clicks = {}
        self.impressions_by_country = defaultdict(int)
        self.clicks_by_country = defaultdict(int)

    def register_impression(
        self,
        uid: str,
        banner: str,
        ip: str,
        country: str | None = None
    ):
        self.impressions[uid] = {
            "uid": uid,
            "banner": banner,
            "ip": ip,
            "country": country,
            "timestamp": datetime.now(timezone.utc),
        }
        if country:
            self.impressions_by_country[country] += 1

    def impression_exists(self, uid: str) -> bool:
        return uid in self.impressions

    def register_click(self, uid: str, ip: str):
        if uid not in self.impressions:
            raise ValueError("Impression not found") 
        country = self.impressions[uid].get("country")
        self.clicks[uid] = {
            "uid": uid,
            "ip": ip,
            "timestamp": datetime.now(timezone.utc),
            "country": country,
        }
        if country:
            self.clicks_by_country[country] += 1

    def click_exists(self, uid: str) -> bool:
        return uid in self.clicks

    def stats(self):
        total_impressions = len(self.impressions)
        total_clicks = len(self.clicks)
        return {
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "ctr": total_clicks / total_impressions if total_impressions else 0,
            "impressions_by_country": dict(self.impressions_by_country),
            "clicks_by_country": dict(self.clicks_by_country),
        }

    def reset(self):
        self.impressions.clear()
        self.clicks.clear()
        self.impressions_by_country.clear()
        self.clicks_by_country.clear()

tracking_db = TrackingDBMock()
