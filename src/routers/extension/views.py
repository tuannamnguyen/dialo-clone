from fastapi import APIRouter

from src.routers.extension.utils import create_extension, get_extensions, delete_extension, update_extension, search_by_name_or_extension
from src.schemas.extension_schema import ExtensionSchema, ExtensionUpdateSchema
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

@extension_router.put("/{extension_id}", response_model=APIResponse)
async def update_one_extension(extension_id: str, update_data: ExtensionUpdateSchema):
    result = await update_extension(extension_id, update_data)
    return result

@extension_router.get("/{extension_id_or_agent_name}", response_model=APIResponse)
async def find_extension_by_id_or_agent_name(extension_id_or_agent_name: str):
    result = await search_by_name_or_extension(extension_id_or_agent_name)
    return result