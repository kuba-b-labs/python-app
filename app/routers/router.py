from fastapi import APIRouter, Request, Response, HTTPException
from ..database.database import postgresDB, Entry
from datetime import date

router = APIRouter()


@router.post("/add/")
async def add_entry(request: Entry):
    """POST entry data to database"""
    async with postgresDB() as db:
        await db.create_entry(request)
    return {"status" : "Entry successfully created"}

@router.get("/entries")
async def get_entries():
    """Get all database entries"""
    async with postgresDB() as db:
        entries = await db.get_entries()
    return entries

@router.get("/entry/{date}")
async def get_entry(date : date):
    """Get database entry"""
    async with postgresDB() as db:
        entries = await db.get_entries(date)
    return entries

@router.put("/entry/")
async def update_entry(entry : Entry):
    """Update database entry"""
    async with postgresDB() as db:
        try:
            await db.update_entry(entry)
        except Exception as error:
            raise HTTPException(detail=f'Entry failed to update : {error}',status_code=500)
    return { "status" : "Entry updated successfully" }

@router.delete("/entry/delete/{entry}")
async def delete_entry(entry : date):
    async with postgresDB() as db:
        try:
            await db.delete_entry(entry)
        except Exception as error:
            raise HTTPException(detail=f'Entry failed to delete: {error}',status_code=500)
    return {"status" : "Entry successfully deleted"}
