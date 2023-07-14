from src.models.extension_model import ExtensionModel
from src.schemas.extension_schema import ExtensionSchema, ExtensionUpdateSchema
from fastapi.encoders import jsonable_encoder
from marshmallow.exceptions import ValidationError
import logging


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


async def get_extensions():
    data = [extension.dump() async for extension in ExtensionModel.find()]
    return {
        "success": True,
        "data": data,
        "message": "Get extensions successfully"
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
        await ExtensionModel.collection.update_one({"extension_id": extension_id}, {"$set": update_data})
        return {
            "success": True,
            "data": update_data,
            "message": "Update extension successfully"
        }
    return {
        "success": False,
        "data": None,
        "message": "Can't find extension"
    }
