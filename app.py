from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime, timezone
import os

app = FastAPI()

@app.get("/me", response_class=JSONResponse)
async def get_profile():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.get("https://catfact.ninja/fact")
            if res.status_code == 200:
                cat_fact = res.json().get("fact", "Cats are awesome!")
            else:
                cat_fact = "Could not fetch cat fact at the moment."
    except Exception:
        cat_fact = "External API unavailable. Try again later."

    data = {
        "status": "success",
        "user": {
            "email": "youremail@example.com",
            "name": "Your Full Name",
            "stack": "Python/FastAPI"
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fact": cat_fact
    }

    return JSONResponse(content=data, media_type="application/json", status_code=status.HTTP_200_OK)