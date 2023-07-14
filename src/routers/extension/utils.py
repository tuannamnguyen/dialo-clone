from src.models.extension_model import ExtensionModel
from src.schemas.extension_schema import ExtensionSchema
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
            "data": ExtensionModel(**request_data).dump(),
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
