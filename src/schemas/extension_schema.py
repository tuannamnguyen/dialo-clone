from pydantic import BaseModel, field_validator, ValidationError

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
        if v and len(v) == 0:
            raise ValueError("Queue list must not be empty")
        return v

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
        if v and len(v) == 0:
            raise ValueError("Queue list must not be empty")
        return v


if __name__ == "__main__":
    try:
        print(ExtensionSchema(extension_id="1123", list_queue_id=["qfqwdqwdqwdqwdqwd"], agent="namnt134", status="Enable", description=None, tenant="5"))
        print(ExtensionSchema(extension_id="1123", list_queue_id=None, agent="namnt134", status="Enable", description=None, tenant="5").model_dump_json())
        print(ExtensionUpdateSchema(list_queue_id=None, agent="namnt134", status=None, description=None, tenant=None))
        

    except ValidationError as e:
        print(e)