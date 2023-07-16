from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, Query

from src.auth.auth_bearer import (JWT_ALGORITHM, JWT_SECRET, jwt_validator,
                                  oauth2_scheme)
from src.schemas.queue_schema import QueueSchema, QueueUpdateSchema
from src.schemas.response_schema import APIResponse
from src.routers.queue.utils import create_queue
queue_router = APIRouter(prefix="/queues", tags=["Queues"])


@queue_router.post("", dependencies=[Depends(jwt_validator)], response_model=APIResponse)
async def create_new_queue(request_data: QueueSchema, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    result = await create_queue(request_data, payload)
    return result