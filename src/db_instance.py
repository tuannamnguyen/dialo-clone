import motor.motor_asyncio
from decouple import config
from umongo.frameworks import MotorAsyncIOInstance

DB_CONNECTION_STRING = config("db_connection_string")

# Connect to DB
client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING)
db = client["dialo_clone"]
instance = MotorAsyncIOInstance(db)