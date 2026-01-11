import subprocess
import sys
import time
import asyncio
import random
import signal
import json
import httpx
import os
from datetime import datetime


API_HOST = "127.0.0.1"
API_PORT = 8000

OTP_URL = f"http://{API_HOST}:{API_PORT}/otp/"
OTP_BILLING_URL = f"http://{API_HOST}:{API_PORT}/otp/billing"
PROVIDER_BILLING_URL = f"http://{API_HOST}:{API_PORT}/sms-provider/billing"
FIREWALL_METRICS_URL = f"http://{API_HOST}:{API_PORT}/metrics/firewall"

REQUESTS_PER_SECOND = 20
CONCURRENT_WORKERS = 5
DURATION_SECONDS = 15
PHONE_REUSE_RATIO = 0.7

OUTPUT_FILE = "metrics_output.json"

USED_PHONES = []


def reset_metrics_file():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"Deleted existing {OUTPUT_FILE}")


def generate_otp():
    return str(random.randint(100000, 999999))


def generate_phone_number():
    prefixes = ["+1", "+52", "+54", "+56", "+57"]
    prefix = random.choice(prefixes)
    number = "".join(str(random.randint(0, 9)) for _ in range(10))
    return f"{prefix}{number}"


def get_target_phone():
    if USED_PHONES and random.random() < PHONE_REUSE_RATIO:
        return random.choice(USED_PHONES)

    phone = generate_phone_number()
    USED_PHONES.append(phone)
    return phone


def start_api():
    print("Starting FastAPI server...")
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            API_HOST,
            "--port",
            str(API_PORT),
        ],
        stdout=None,
        stderr=None,
    )


async def wait_for_api():
    async with httpx.AsyncClient() as client:
        for _ in range(20):
            try:
                r = await client.get(f"http://{API_HOST}:{API_PORT}/docs")
                if r.status_code == 200:
                    return
            except Exception:
                pass
            await asyncio.sleep(0.5)
    raise RuntimeError("API did not start")


async def send_otp(client):
    payload = {
        "phone": get_target_phone(),
        "code": generate_otp(),
    }
    await client.post(OTP_URL, json=payload)


async def attack_worker(end_time):
    async with httpx.AsyncClient() as client:
        while time.time() < end_time:
            await send_otp(client)
            await asyncio.sleep(1 / REQUESTS_PER_SECOND)


async def run_attack():
    end_time = time.time() + DURATION_SECONDS
    await asyncio.gather(
        *[attack_worker(end_time) for _ in range(CONCURRENT_WORKERS)]
    )


async def collect_metrics():
    async with httpx.AsyncClient() as client:
        otp_billing = (await client.get(OTP_BILLING_URL)).json()
        provider_billing = (await client.get(PROVIDER_BILLING_URL)).json()
        firewall_metrics = (await client.get(FIREWALL_METRICS_URL)).json()

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "attack_config": {
            "rps": REQUESTS_PER_SECOND,
            "workers": CONCURRENT_WORKERS,
            "duration": DURATION_SECONDS,
            "phone_reuse_ratio": PHONE_REUSE_RATIO,
            "unique_phones": len(set(USED_PHONES)),
        },
        "otp_billing": otp_billing,
        "provider_billing": provider_billing,
        "firewall_metrics": firewall_metrics,
    }


def save_metrics(data):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Metrics exported to {OUTPUT_FILE}")


async def main():
    reset_metrics_file()
    api = start_api()
    try:
        await wait_for_api()
        await run_attack()
        metrics = await collect_metrics()
        save_metrics(metrics)
    finally:
        api.send_signal(signal.SIGINT)
        api.wait()


if __name__ == "__main__":
    asyncio.run(main())
