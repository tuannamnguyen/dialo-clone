from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, Query

from src.auth.auth_bearer import (JWT_ALGORITHM, JWT_SECRET, jwt_validator,
                                  oauth2_scheme)
from src.routers.extension.utils import (create_extension, delete_extension,
                                         get_extensions,
                                         search_by_name_or_extension,
                                         update_extension)
from src.schemas.extension_schema import ExtensionSchema, ExtensionUpdateSchema
from src.schemas.response_schema import APIResponse

extension_router = APIRouter(prefix="/extensions", tags=["Extensions"])


@extension_router.post("", dependencies=[Depends(jwt_validator)], response_model=APIResponse)
async def create_new_extension(request_data: ExtensionSchema, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    result = await create_extension(request_data, payload)
    return result


@extension_router.get("", dependencies=[Depends(jwt_validator)], response_model=APIResponse)
async def get_all_extensions(token: Annotated[str, Depends(oauth2_scheme)],
                             queue: Annotated[list[str], Query()] = [],
                             status: Annotated[str | None, Query(regex=r'\b(?:Enable|Disable)\b')] = None):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    result = await get_extensions(queue, status, payload)
    return result


@extension_router.delete("/{extension_id}", dependencies=[Depends(jwt_validator)], response_model=APIResponse)
async def delete_one_extension(extension_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    result = await delete_extension(extension_id, payload)
    return result


@extension_router.put("/{extension_id}", dependencies=[Depends(jwt_validator)], response_model=APIResponse)
async def update_one_extension(extension_id: str, update_data: ExtensionUpdateSchema, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    result = await update_extension(extension_id, update_data, payload)
    return result


@extension_router.get("/{extension_id_or_agent_name}", dependencies=[Depends(jwt_validator)], response_model=APIResponse)
async def find_extension_by_id_or_agent_name(extension_id_or_agent_name: str, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    result = await search_by_name_or_extension(extension_id_or_agent_name, payload)
    return result
