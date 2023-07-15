from src.models.extension_model import ExtensionModel
from src.schemas.extension_schema import ExtensionSchema, ExtensionUpdateSchema
from fastapi.encoders import jsonable_encoder
from marshmallow.exceptions import ValidationError
from pymongo.errors import DuplicateKeyError


async def create_extension(request_data: ExtensionSchema):
    try:
        await ExtensionModel.ensure_indexes()
        request_data = jsonable_encoder(request_data)
        await ExtensionModel(**request_data).commit()
        return {
            "success": True,
            "data": request_data,
            "message": "Add new extension successfully"
        }
    except ValidationError as e:
        print(e)
        return {
            "success": False,
            "data": None,
            "message": "Extension already existed"
        }


async def get_extensions(queue: list[str], status: str):
    data = []
    if not queue and not status:
        data = [extension.dump() async for extension in ExtensionModel.find()]
    elif queue and not status:
        data = [extension.dump() async for extension in ExtensionModel.find(
            {"list_queue_id": {"$elemMatch": {"$in": queue}}}
        )]
    elif status and not queue:
        data = [extension.dump() async for extension in ExtensionModel.find(
            {"status": status}
        )]
    elif queue and status:
        data = [extension.dump() async for extension in ExtensionModel.find(
            {"$and": [{"list_queue_id": {"$elemMatch": {"$in": queue}}}, {
                "status": status}]}
        )]

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


async def delete_extension(extension_id: str):
    extension = await ExtensionModel.find_one({"extension_id": extension_id})
    if extension:
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


async def update_extension(extension_id: str, update_data: ExtensionUpdateSchema):
    extension = await ExtensionModel.find_one({"extension_id": extension_id})
    if extension:
        update_data = jsonable_encoder(update_data)
        update_data = {k: v for k, v in update_data.items() if v is not None}
        try:
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
                "message": "Duplicate agent or extension ID"
            }
    return {
        "success": False,
        "data": None,
        "message": "Can't find extension"
    }


async def search_by_name_or_extension(param: str):
    extension = await ExtensionModel.find_one({"$or": [{"extension_id": param}, {"agent": param}]})
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
