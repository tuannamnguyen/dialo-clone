from pydantic import BaseModel, ValidationError, field_validator

class QueueSchema(BaseModel):
    queue_id: str
    list_extension_id: list[str] | None = None
    description: str | None = None
    tenant: str

    @field_validator("list_extension_id")
    # TODO: test
    def extension_must_exist(cls, v):
        if v and len(v) == 0:
            raise ValueError("Extension list must not be empty")
        return v


class QueueUpdateSchema(BaseModel):
    queue_id: None = None
    list_extension_id: list[str] | None = None
    description: str | None = None
    tenant: None = None

    @field_validator("list_extension_id")
    # TODO: test
    def extension_must_exist(cls, v):
        if v and len(v) == 0:
            raise ValueError("Extension list must not be empty")
        return v

if __name__ == "__main__":
    try:
        print(QueueSchema(queue_id="651165", list_extension_id=["asdasca", "ascascascas"], description=None, tenant="1").model_dump_json())

    except ValidationError as e:
        print(e)