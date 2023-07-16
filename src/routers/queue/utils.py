from fastapi.encoders import jsonable_encoder
from marshmallow.exceptions import ValidationError
from pymongo.errors import DuplicateKeyError

from src.models.extension_model import ExtensionModel
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

        queue_model = QueueModel(**request_data)
        list_extension_id = queue_model.list_extension_id
        if list_extension_id: # check is list_extension_id is not empty
            # ensure list_extension_id does not have duplicate values
            list_extension_id = list(set(list_extension_id))

            # ensure that each extension in list_extension_id exists
            if len(list_extension_id) != await ExtensionModel.count_documents({"extension_id": {"$in": list_extension_id}}):
                return {
                    "success": False,
                    "data": None,
                    "message": "One or more extensions does not exist"
                }

            # for each extension in list_extension_id, append queue_id to list_queue_id
            ExtensionModel.collection.update_many(
                {"extension_id": {"$in": list_extension_id}},
                {"$push": {"list_queue_id": queue_model.queue_id}}
            )

        await queue_model.commit()
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
        list_extension_id = queue.list_extension_id
        if list_extension_id: # check if list_extension_id is not empty
            # ensure list_queue_id does not have duplicate values
            list_extension_id = list(set(list_extension_id))
            
            # for each extension in list_extension_id, delete queue_id from list_queue_id
            ExtensionModel.collection.update_many(
                {"extension_id": {"$in": list_extension_id}},
                {"$pull": {"list_queue_id": queue_id}}
            )

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
            if update_data["list_extension_id"]: # check if list_extension_id is not empty
                # ensure list_extension_id does not have duplicate values
                update_data["list_extension_id"] = list(
                    set(update_data["list_extension_id"]))
                new_list_extension_id = update_data["list_extension_id"]
                old_list_extension_id = queue.list_extension_id

                # 1. For each extension in old list_extension_id, delete queue from list_queue_id
                if old_list_extension_id: # check if old list is not empty
                    old_list_extension_id = list(set(old_list_extension_id))
                    ExtensionModel.collection.update_many(
                        {"extension_id": {"$in": old_list_extension_id}},
                        {"$pull": {"list_queue_id": queue_id}}
                    )

                # ensure that each extension in new_list_extension_id exists
                if len(new_list_extension_id) != await ExtensionModel.count_documents({"extension_id": {"$in": new_list_extension_id}}):
                    return {
                        "success": False,
                        "data": None,
                        "message": "One or more extensions does not exist"
                    }

                # 2. For each extension in new list_extension_id, add queue to list_queue_id
                ExtensionModel.collection.update_many(
                    {"extension_id": {"$in": new_list_extension_id}},
                    {"$push": {"list_queue_id": queue_id}}
                )
                
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
