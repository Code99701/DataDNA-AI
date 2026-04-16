"""
MongoDB connection manager using motor (async driver).
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI, MONGO_DB_NAME

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient = None
db = None


async def connect_db():
    """Open the MongoDB connection and select the database."""
    global client, db
    logger.info("Connecting to MongoDB at %s ...", MONGO_URI)
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    # Quick connectivity check
    await client.admin.command("ping")
    logger.info("MongoDB connected — database: %s", MONGO_DB_NAME)


async def close_db():
    """Gracefully close the MongoDB connection."""
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed.")


def get_db():
    """Return the current database handle."""
    return db
