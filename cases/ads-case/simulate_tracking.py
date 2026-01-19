import asyncio
import httpx
import random
import json
import uvicorn
from app.main import app

API_HOST = "127.0.0.1"
API_PORT = 8002
API_BASE = f"http://{API_HOST}:{API_PORT}/banner"
IMAGE_NAME = "example.png"
NUM_IMPRESSIONS = 5000
CLICK_PROBABILITY = 0.6
CONCURRENT_REQUESTS = 100


async def run_server():
    config = uvicorn.Config(app, host=API_HOST, port=API_PORT, log_level="warning")
    server = uvicorn.Server(config)
    await server.serve()

async def fetch_impression(client):
    resp = await client.get(f"{API_BASE}/impression/{IMAGE_NAME}", follow_redirects=False)
    return resp.headers.get("X-Request-UID")


async def simulate_impressions(client):
    uids = []

    for i in range(0, NUM_IMPRESSIONS, CONCURRENT_REQUESTS):
        batch_size = min(CONCURRENT_REQUESTS, NUM_IMPRESSIONS - i)
        tasks = [fetch_impression(client) for _ in range(batch_size)]
        results = await asyncio.gather(*tasks)
        uids.extend([uid for uid in results if uid])
        print(f"Registered impressions: {len(uids)}/{NUM_IMPRESSIONS}", end="\r")

    print() 
    return uids

async def simulate_clicks(client, uids):
    clicks_to_send = [uid for uid in uids if random.random() < CLICK_PROBABILITY]
    total_clicks = len(clicks_to_send)
    clicks_done = 0

    async def send_click(uid):
        nonlocal clicks_done
        await client.get(f"{API_BASE}/click/{uid}")
        clicks_done += 1
        print(f"Simulated clicks: {clicks_done}/{total_clicks}", end="\r")

    for i in range(0, total_clicks, CONCURRENT_REQUESTS):
        batch = clicks_to_send[i:i+CONCURRENT_REQUESTS]
        tasks = [send_click(uid) for uid in batch]
        await asyncio.gather(*tasks)

    print()
    return total_clicks

async def simulate_client():
    async with httpx.AsyncClient() as client:
        uids = await simulate_impressions(client)
        total_clicks = await simulate_clicks(client, uids)

        stats_resp = await client.get(f"{API_BASE}/stats")
        stats_data = stats_resp.json()

        filename = f"stats.json"
        with open(filename, "w") as f:
            json.dump(stats_data, f, indent=4)
        print(f"File {filename} generated")
        print(f"Total clicks simulated: {total_clicks}")


async def main():
    config = uvicorn.Config(app, host=API_HOST, port=API_PORT, log_level="warning")
    server = uvicorn.Server(config)
    server_task = asyncio.create_task(server.serve())

    await asyncio.sleep(1)

    await simulate_client()

    server.should_exit = True
    await server_task
    print("Server stopped gracefully")

if __name__ == "__main__":
    asyncio.run(main())
