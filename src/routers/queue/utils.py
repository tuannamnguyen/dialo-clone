from fastapi.encoders import jsonable_encoder
from marshmallow.exceptions import ValidationError
from pymongo.errors import DuplicateKeyError

from src.models.queue_model import QueueModel
from src.schemas.queue_schema import QueueSchema, QueueUpdateSchema

TENANT_ERROR = "Different tenant. Operation failed"


async def create_queue(request_data: QueueSchema, payload: dict):
    tenant = payload.get("tenant_id")
    try:
        await QueueModel.ensure_indexes()
        request_data = jsonable_encoder(request_data)
        if tenant != request_data.get("tenant"):
            return {
                "success": False,
                "data": None,
                "message": TENANT_ERROR
            }
        await QueueModel(**request_data).commit()
        return {
            "success": True,
            "data": request_data,
            "message": "Add new queue successfully"
        }

    except ValidationError as e:
        print(e)
        return {
            "success": False,
            "data": None,
            "message": str(e)
        }


async def get_queue(payload: dict):
    tenant = payload.get("tenant_id")
    data = [queue.dump() async for queue in QueueModel.find({"tenant": tenant})]

    if data:
        return {
            "success": True,
            "data": data,
            "message": "Get queues successfully"
        }
    return {
        "success": False,
        "data": None,
        "message": "Can't find any queue"
    }


async def delete_queue(queue_id: str, payload: dict):
    tenant = payload.get("tenant_id")
    queue = await QueueModel.find_one({"queue_id": queue_id})
    if queue:
        if queue.tenant != tenant:
            return {
                "success": False,
                "data": None,
                "message": TENANT_ERROR
            }
        await QueueModel.collection.delete_one({"queue_id": queue_id})
        return {
            "success": True,
            "data": queue.dump(),
            "message": "Delete queue successfully"
        }
    return {
        "success": False,
        "data": None,
        "message": "Can't find queue"
    }


async def update_queue(queue_id: str, update_data: QueueUpdateSchema, payload: dict):
    tenant = payload.get("tenant_id")
    queue = await QueueModel.find_one({"queue_id": queue_id})
    if queue:
        if queue.tenant != tenant:
            return {
                "success": False,
                "data": None,
                "message": TENANT_ERROR
            }
        update_data = jsonable_encoder(update_data)
        update_data = {k: v for k, v in update_data.items() if v is not None}
        try:
            await QueueModel.collection.update_one({"queue_id": queue_id}, {"$set": update_data})
            return {
                "success": True,
                "data": update_data,
                "message": "Update extension successfully"
            }
        except DuplicateKeyError as e:
            print(e)
            return {
                "success": False,
                "data": None,
                "message": str(e)
            }


async def search_by_id_or_extension(param: str, payload: dict):
    tenant = payload.get("tenant_id")
    queue = await QueueModel.find_one({
        "$and": [
            {"tenant": tenant},
            {"$or": [
                {"queue_id": param},
                {"list_extension_id": param}
            ]}
        ]
    })

    if queue:
        return {
            "success": True,
            "data": queue.dump(),
            "message": "Queue found"
        }
    return {
        "success": False,
        "data": None,
        "message": "Can't find queue"
    }
