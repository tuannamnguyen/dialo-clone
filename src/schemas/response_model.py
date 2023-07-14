from pydantic import BaseModel
from typing import Any

class APIResponse(BaseModel):
    success: bool = False
    data: Any
    message: str