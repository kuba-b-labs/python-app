from fastapi import APIRouter, Request, Response, HTTPException
from ..database.database import postgresDB, Entry
from typing import Annotated
from datetime import date
import logging
from azure.monitor.opentelemetry import configure_azure_monitor
#from os import getenv
from dotenv import load_dotenv

load_dotenv()
#set up logger name and formatter
configure_azure_monitor(
    logger_name = "azure_logger",
    logging_formatter=logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger = logging.getLogger("azure_logger")
logger.setLevel(logging.INFO)
router = APIRouter()


@router.post("/add/")
async def add_entry(request: Entry):
    """POST entry data to database"""
    async with postgresDB() as db:
        try:
            await db.create_entry(request)
            logger.info("Entry added")
        except Exception as error:
            logger.error(error)
            raise HTTPException(detail=f'Failed to add entry: {error}',status_code=500)
    return {"status" : "Entry successfully created"}

@router.get("/entries")
async def get_entries():
    """Get all database entries"""
    async with postgresDB() as db:
        try:            
            entries = await db.get_entries()
            logger.info("All entries pulled")
        except Exception as error:
            logger.info(error)
            raise HTTPException(detail=f'Failed to get entries: {error}',status_code=500)
    return entries

@router.get("/entry/{date}")
async def get_entry(date : date):
    """Get database entry"""
    async with postgresDB() as db:
        try:
            entries = await db.get_entries(date)
            logger.info("Query for entry successfull") 
        except Exception as error:
            logger.error(error)
            raise HTTPException(detail=f'Failed to get all entries: {error}',status_code=500)
    return entries

@router.put("/entry/")
async def update_entry(entry : Entry, q : bool = 0):
    """Update database calorie intake entry"""
    async with postgresDB() as db:
        try:
            await db.update_entry(entry, q)
            logger.info("Entry successfully updated")
        except Exception as error:
            logger.error(error)
            raise HTTPException(detail=f'Entry failed to update: {error}',status_code=500)
    return { "status" : "Entry updated successfully" }

@router.delete("/entry/delete/{entry}")
async def delete_entry(entry : date):
    async with postgresDB() as db:
        try:
            await db.delete_entry(entry)
            logger.info("Entry successfully deleted")
        except Exception as error:
            logger.error 
            raise HTTPException(detail=f'Entry failed to delete: {error}',status_code=500)
    return {"status" : "Entry successfully deleted"}
