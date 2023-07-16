from fastapi.encoders import jsonable_encoder
from marshmallow.exceptions import ValidationError
from pymongo.errors import DuplicateKeyError

from src.models.extension_model import ExtensionModel
from src.models.queue_model import QueueModel
from src.schemas.extension_schema import ExtensionSchema, ExtensionUpdateSchema

TENANT_ERROR = "Different tenant. Operation failed"


async def create_extension(request_data: ExtensionSchema, payload: dict):
    tenant = payload.get("tenant_id")
    try:
        await ExtensionModel.ensure_indexes()
        request_data = jsonable_encoder(request_data)

        if tenant != request_data.get("tenant"):
            return {
                "success": False,
                "data": None,
                "message": TENANT_ERROR
            }

        extension_model = ExtensionModel(**request_data)
        list_queue_id = extension_model.list_queue_id
        if list_queue_id:
            # ensure list_queue_id does not have duplicate values
            list_queue_id = list(set(list_queue_id))
            # for each queue in list_queue_id, append extension_id to list_extension_id
            QueueModel.collection.update_many(
                {"queue_id": {"$in": list_queue_id}},
                {"$push": {"list_extension_id": extension_model.extension_id}}
            )

        await extension_model.commit()
        return {
            "success": True,
            "data": request_data,
            "message": "Add new extension successfully"
        }
    except ValidationError as e:
        return {
            "success": False,
            "data": None,
            "message": str(e)
        }


async def get_extensions(queue: list[str], status: str, payload: dict):
    tenant = payload.get("tenant_id")
    data = []
    if not queue and not status:
        data = [extension.dump() async for extension in ExtensionModel.find({"tenant": tenant})]
    elif queue and not status:
        data = [extension.dump() async for extension in ExtensionModel.find({
            "$and": [
                {"tenant": tenant},
                {"list_queue_id": {"$elemMatch": {"$in": queue}}}
            ]
        })]
    elif status and not queue:
        data = [extension.dump() async for extension in ExtensionModel.find({
            "$and": [
                {"status": status}, {"tenant": tenant}
            ]
        })]
    elif queue and status:
        data = [extension.dump() async for extension in ExtensionModel.find({
            "$and": [{"list_queue_id": {"$elemMatch": {"$in": queue}}},
                     {"status": status}]
        })]

    if data:
        return {
            "success": True,
            "data": data,
            "message": "Get extensions successfully"
        }
    return {
        "success": False,
        "data": None,
        "message": "Can't find any extension"
    }


async def delete_extension(extension_id: str, payload: dict):
    tenant = payload.get("tenant_id")
    extension = await ExtensionModel.find_one({"extension_id": extension_id})
    if extension:
        if extension.tenant != tenant:
            return {
                "success": False,
                "data": None,
                "message": TENANT_ERROR
            }
        list_queue_id = extension.list_queue_id
        if list_queue_id:
            # ensure list_queue_id does not have duplicate values
            list_queue_id = list(set(list_queue_id))
            # for each queue in list_queue_id, delete extension_id from list_extension_id
            QueueModel.collection.update_many(
                {"queue_id": {"$in": list_queue_id}},
                {"$pull": {"list_extension_id": extension_id}}
            )
        await ExtensionModel.collection.delete_one({"extension_id": extension_id})
        return {
            "success": True,
            "data": extension.dump(),
            "message": "Delete extension successfully"
        }
    return {
        "success": False,
        "data": None,
        "message": "Can't find extension"
    }


async def update_extension(extension_id: str, update_data: ExtensionUpdateSchema, payload: dict):
    tenant = payload.get("tenant_id")
    extension = await ExtensionModel.find_one({"extension_id": extension_id})
    if extension:
        if extension.tenant != tenant:
            return {
                "success": False,
                "data": None,
                "message": TENANT_ERROR
            }
        update_data = jsonable_encoder(update_data)
        update_data = {k: v for k, v in update_data.items() if v is not None}
        try:
            if update_data["list_queue_id"]:
                # ensure list_queue_id does not have duplicate values
                update_data["list_queue_id"] = list(
                    set(update_data["list_queue_id"]))
                new_list_queue_id = update_data["list_queue_id"]
                old_list_queue_id = extension.list_queue_id

                # 1. For each queue in old list_queue_id, delete extension from list_extension_id
                if old_list_queue_id:
                    old_list_queue_id = list(set(old_list_queue_id))
                    QueueModel.collection.update_many(
                        {"queue_id": {"$in": old_list_queue_id}},
                        {"$pull": {"list_extension_id": extension_id}}
                    )
                # 2. For each queue in new list_queue_id, add extension to list_extension_id
                QueueModel.collection.update_many(
                {"queue_id": {"$in": new_list_queue_id}},
                {"$push": {"list_extension_id": extension_id}}
            )
            await ExtensionModel.collection.update_one({"extension_id": extension_id}, {"$set": update_data})
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
    return {
        "success": False,
        "data": None,
        "message": "Can't find extension"
    }


async def search_by_name_or_extension(param: str, payload: dict):
    tenant = payload.get("tenant_id")
    extension = await ExtensionModel.find_one({
        "$and": [{"tenant": tenant},
                 {"$or": [{"extension_id": param}, {"agent": param}]
                  }]
    })
    if extension:
        return {
            "success": True,
            "data": extension.dump(),
            "message": "Extension found"
        }
    return {
        "success": False,
        "data": None,
        "message": "Can't find any extension"
    }
