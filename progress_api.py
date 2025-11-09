"""
Simple progress sync API for cross-device progress tracking.
This can be deployed as a separate service or integrated into the main app.
"""
import json
import os
from typing import Optional

import httpx

# Use a free cloud storage service or your own backend
# Option 1: Use JSONBin.io (free tier available)
# Option 2: Use your own backend API endpoint
PROGRESS_API_URL = os.getenv("PROGRESS_API_URL", "https://api.jsonbin.io/v3/b")

# JSONBin.io requires an API key (free at jsonbin.io)
JSONBIN_API_KEY = os.getenv("JSONBIN_API_KEY", "")
JSONBIN_BIN_ID = os.getenv("JSONBIN_BIN_ID", "")


async def load_progress_cloud(user_id: str, exercise_key: str) -> tuple[int, int]:
    """Load progress from cloud storage."""
    if not user_id:
        return 0, 0
    
    try:
        if JSONBIN_API_KEY and JSONBIN_BIN_ID:
            # Use JSONBin.io
            url = f"{PROGRESS_API_URL}/{JSONBIN_BIN_ID}/latest"
            headers = {
                "X-Master-Key": JSONBIN_API_KEY,
                "Content-Type": "application/json",
            }
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=5.0)
                if response.status_code == 200:
                    data = response.json().get("record", {})
                    user_data = data.get(user_id, {})
                    exercise_data = user_data.get(exercise_key, {})
                    return int(exercise_data.get("score", 0)), int(exercise_data.get("total", 0))
    except Exception:
        pass
    
    return 0, 0


async def save_progress_cloud(user_id: str, exercise_key: str, score: int, total: int) -> bool:
    """Save progress to cloud storage."""
    if not user_id:
        return False
    
    try:
        if JSONBIN_API_KEY and JSONBIN_BIN_ID:
            headers = {
                "X-Master-Key": JSONBIN_API_KEY,
                "Content-Type": "application/json",
            }
            
            async with httpx.AsyncClient() as client:
                # Get current data
                get_url = f"{PROGRESS_API_URL}/{JSONBIN_BIN_ID}/latest"
                response = await client.get(get_url, headers=headers, timeout=5.0)
                if response.status_code == 200:
                    data = response.json().get("record", {})
                else:
                    data = {}
                
                # Update user's progress
                if user_id not in data:
                    data[user_id] = {}
                data[user_id][exercise_key] = {"score": score, "total": total}
                
                # Save back
                put_url = f"{PROGRESS_API_URL}/{JSONBIN_BIN_ID}"
                put_response = await client.put(put_url, json=data, headers=headers, timeout=5.0)
                return put_response.status_code in [200, 201]
    except Exception:
        pass
    
    return False

