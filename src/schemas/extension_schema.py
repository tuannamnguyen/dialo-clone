from pydantic import BaseModel, field_validator, ValidationError
from src.models.queue_model import QueueModel

class ExtensionSchema(BaseModel):
    extension_id: str
    list_queue_id: list[str] | None = None
    agent: str | None = None
    status: str | None = None
    description: str | None = None
    tenant: str

    @field_validator("extension_id")
    def id_must_contain_numbers_only(cls, v):
        if not v.isnumeric():
            raise ValueError("Must contain number only")
        return v
    
    @field_validator("status")
    def must_have_valid_status(cls, v):
        if v != "Enable" and v != "Disable" and v is not None:
            raise ValueError("Invalid status")
        return v
    
    @field_validator("list_queue_id")
    # TODO: test
    def queue_must_exist(cls, v):
        if len(v) == 0:
            raise ValueError("Queue list must not be empty")
        if len(list(set(v))) != QueueModel.count_documents({"queue_id": {"$in": v}}):
            raise ValueError("One or more queues does not exist")

class ExtensionUpdateSchema(BaseModel):
    extension_id: None = None
    list_queue_id: list[str] | None = None
    agent: str | None = None
    status: str | None = None
    description: str | None = None
    tenant: None = None

    @field_validator("status")
    def must_have_valid_status(cls, v):
        if v != "Enable" and v != "Disable" and v is not None:
            raise ValueError("Invalid status")
        return v
    
    @field_validator("list_queue_id")
    # TODO: test
    def queue_must_exist(cls, v):
        if len(v) == 0:
            raise ValueError("Queue list must not be empty")
        if len(v) != QueueModel.count_documents({"queue_id": {"$in": v}}):
            raise ValueError("One or more queue does not exist")


if __name__ == "__main__":
    try:
        print(ExtensionSchema(extension_id="1123", list_queue_id=[], agent="namnt134", status="Enable", description=None))
        print(ExtensionSchema(extension_id="1123", list_queue_id=[], agent="namnt134", status="Enable", description=None).model_dump_json())
        print(ExtensionUpdateSchema(list_queue_id=[], agent="namnt134", status=None, description=None, tenant="5"))
        

    except ValidationError as e:
        print(e)