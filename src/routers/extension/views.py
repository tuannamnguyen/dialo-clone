from fastapi import APIRouter

from src.routers.extension.utils import create_extension, get_extensions, delete_extension
from src.schemas.extension_schema import ExtensionSchema
from src.schemas.response_model import APIResponse

extension_router = APIRouter(prefix="/extensions", tags=["Extensions"])


@extension_router.post("", response_model=APIResponse)
async def create_new_extension(request_data: ExtensionSchema):
    result = await create_extension(request_data)
    return result

@extension_router.get("", response_model=APIResponse)
async def get_all_extensions():
    result = await get_extensions()
    return result

@extension_router.delete("/{extension_id}", response_model=APIResponse)
async def delete_one_extension(extension_id: str):
    result = await delete_extension(extension_id)
    return result