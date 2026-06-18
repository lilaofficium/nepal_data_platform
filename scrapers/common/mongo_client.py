from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI, MONGO_DB_NEPSE
from scrapers.common.logger import get_logger

logger = get_logger(__name__)

client = MongoClient(MONGO_URI)
db     = client[MONGO_DB_NEPSE]

def save_one(collection: str, record: dict) -> None:
    record["scraped_at"] = datetime.utcnow().isoformat()
    db[collection].insert_one(record)
    logger.info(f"Saved 1 document → {collection}")

def save_many(collection: str, records: list) -> None:
    if not records:
        logger.warning(f"No records to save → {collection}")
        return
    for r in records:
        r["scraped_at"] = datetime.utcnow().isoformat()
    db[collection].insert_many(records)
    logger.info(f"Saved {len(records)} documents → {collection}")

def collection_exists(collection: str) -> bool:
    return collection in db.list_collection_names()

def get_collection(collection: str):
    return db[collection]