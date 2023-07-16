from src.models.queue_model import QueueModel
from src.schemas.queue_schema import QueueSchema
from marshmallow.exceptions import ValidationError
from fastapi.encoders import jsonable_encoder


async def create_queue(request_data: QueueSchema, payload: dict):
    tenant = payload.get("tenant_id") 
    try:
        await QueueModel.ensure_indexes()
        request_data = jsonable_encoder(request_data)
        if tenant != request_data.get("tenant"):
            return {
                "success": False,
                "data": None,
                "message": "Different tenant. Operation failed"
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

