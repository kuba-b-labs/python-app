import asyncpg
import asyncio
import logging
from datetime import datetime, date
from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel, Field

load_dotenv()

class Entry(BaseModel):
    weight : float
    calorie_intake: int | None = None
    input_date : date | None = None

class postgresDB():
    """database commands execution"""

    async def __aenter__(self):
        """OPEN CONNECTION TO DATABASE"""
        self.pool = await asyncpg.create_pool(getenv("DATABASE_URL"))
        logging.info("database connection established")
        return self #must return self so async with block assigns the instance
    
    async def __aexit__(self,exc_type, exc_value, traceback):
        """CLOSE CONNECTION TO DATABASE"""
        await self.pool.close()
        logging.info("database connection closed")

    def convert_to_datetime(self, query_date):
        query_date = datetime.strptime(query_date, "%Y-%m-%d").date()
        return query_date

    async def get_entries(self,query_date : date | None = None):
        """GET ALL ENTRIES IN DATABASE or SPECIFIC DATE ENTRY"""
        async with self.pool.acquire() as con:
            if query_date:
                if isinstance(query_date, str):
                   query_date = self.convert_to_datetime(query_date)
                ask_query = """
                    SELECT * FROM entries
                    WHERE DATE = $1
                    ;""" 
                try:
                    db_rows = await con.fetch(ask_query,query_date)
                    logging.info("Query 'get all entries' executed")
                except Exception as error:
                    logging.error(error)
            else:
                ask_query = """
                    SELECT * FROM entries;
                """
                try:
                    db_rows = await con.fetch(ask_query)
                    logging.info("Query 'get entry' executed")
                except Exception as error:
                    logging.error(error)
            entries = [
                {
                    key: value.isoformat() if isinstance(value, date) else value
                    for key, value in dict(row).items()
                }
                for row in db_rows
            ]
        return entries
    
    async def create_entry(self, entry : Entry):
        """CREATE NEW ENTRY"""
        async with self.pool.acquire() as con:
            if entry.input_date is None:
                entry.input_date = date.today()
            ask_query = """INSERT INTO ENTRIES(WEIGHT,DATE, CALORIE_INTAKE) VALUES ($1, $2, $3)"""
            try:
                await con.execute(ask_query, entry.weight, entry.input_date, entry.calorie_intake)
                logging.info("Create entry query executed")
            except Exception as error:
                logging.error(error)
        return f'Entry successfully added'
    
    async def delete_entry(self, date_to_delete : date):
        """DELETE ENTRIES"""
        async with self.pool.acquire() as con:
            check_if_exist = await self.get_entries(date_to_delete)
            if check_if_exist:
                delete_query = """DELETE FROM ENTRIES WHERE DATE = $1;"""
                try:
                    await con.execute(delete_query, date_to_delete)
                    logging.info("Delete query executed")
                except Exception as error:
                    logging.error(error)
                return f'Entry successfully deleted'
            return f'Entry not found in database'
            
    async def update_entry(self, entry_to_update : Entry, q : bool):
        """UPDATE SPECIFIC ENTRY"""
        async with self.pool.acquire() as con:
            check_if_exist = await self.get_entries(entry_to_update.input_date)
            if check_if_exist:
                if q:
                    update_query = """UPDATE ENTRIES SET WEIGHT = $1 WHERE DATE = $2;"""
                    try:
                        await con.execute(update_query, entry_to_update.weight, entry_to_update.input_date)
                        logging.info("Update query executed")
                    except Exception as error:
                        logging.error(error)
                else:
                    update_query = """UPDATE ENTRIES SET CALORIE_INTAKE = $1 WHERE DATE = $2;"""
                    try:
                        await con.execute(update_query, entry_to_update.calorie_intake, entry_to_update.input_date)
                        logging.info("Update query executed")
                    except Exception as error:
                        logging.error(error)
                return f'Entry successfully updated'
            return f'Entry not found in database'

