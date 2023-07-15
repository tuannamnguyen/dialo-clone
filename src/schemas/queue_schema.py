from pydantic import BaseModel

class QueueSchema(BaseModel):
    queue_id: str
    list_extension_id: list[str] | None = None
    description: str | None = None
    tenant: str | None = None

class QueueUpdateSchema(BaseModel):
    queue_id: None = None
    list_extension_id: list[str] | None = None
    description: str | None = None
    tenant: None = None