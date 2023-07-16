from pydantic import BaseModel, ValidationError

class QueueSchema(BaseModel):
    queue_id: str
    list_extension_id: list[str] | None = None
    description: str | None = None
    tenant: str

class QueueUpdateSchema(BaseModel):
    queue_id: None = None
    list_extension_id: list[str] | None = None
    description: str | None = None
    tenant: None = None

if __name__ == "__main__":
    try:
        print(QueueSchema(queue_id="651165", list_extension_id=["asdasd", "asdasda"], description=None, tenant="1").model_dump_json())

    except ValidationError as e:
        print(e)