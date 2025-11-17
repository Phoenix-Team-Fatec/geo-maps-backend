from datetime import datetime
from typing import Optional
from bson import ObjectId
from app.core.database import db 
from pymongo import ASCENDING, DESCENDING

reset_tokens_collection = db["reset_tokens"]

# Chame isso uma única vez no startup
async def ensure_reset_indexes():
    await reset_tokens_collection.create_index(
        [("expires_at", ASCENDING)], expireAfterSeconds=0
    )
    await reset_tokens_collection.create_index([("user_id", ASCENDING)], background=True)
    await reset_tokens_collection.create_index([("created_at", DESCENDING)], background=True)

async def create_reset_token(user_id, code_hash: str, expires_at: datetime):
    doc = {
        "user_id": user_id,
        "code_hash": code_hash,        
        "created_at": datetime.utcnow(),
        "expires_at": expires_at,
        "attempts": 0,
        "used": False,
    }
    await reset_tokens_collection.insert_one(doc)


async def get_active_token(user_id) -> Optional[dict]:
    # pega o MAIS recente ainda válido e não usado
    return await reset_tokens_collection.find_one(
        {
            "user_id": user_id,
            "used": False,
            "expires_at": {"$gt": datetime.utcnow()},
        },
        sort=[("created_at", DESCENDING)],
        projection={"code_hash": 1, "attempts": 1, "_id": 1}
    )

async def increment_attempts(token_id):
    await reset_tokens_collection.update_one({"_id": token_id}, {"$inc": {"attempts": 1}})

async def mark_used(token_id):
    await reset_tokens_collection.update_one({"_id": token_id}, {"$set": {"used": True}})
