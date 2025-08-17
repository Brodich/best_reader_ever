import httpx
async def register_user(tg_id: str, username: str):
    url = "https://prototype.bytecode.su/api/v1/user"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "tg_id": tg_id,
        "username": username
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None