from pydantic import BaseModel, field_validator, ValidationError

class ExtensionSchema(BaseModel):
    extension_id: str
    list_queue_id: list[str] | None = None
    agent: str | None = None
    status: str | None = None
    description: str | None = None

    @field_validator("extension_id")
    def id_must_contain_numbers_only(cls, v):
        if not v.isnumeric():
            raise ValueError("Must contain number only")
        return v
    
    @field_validator("status")
    def must_have_valid_status(cls, v):
        if v != "Enable" and v != "Disable":
            raise ValueError("Invalid status")
        return v
        

if __name__ == "__main__":
    try:
        print(ExtensionSchema(extension_id="1123", list_queue_id=[], agent="namnt134", status="Enable", description=None))
    except ValidationError as e:
        print(e)