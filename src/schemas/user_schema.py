from pydantic import BaseModel, field_validator


class UserSchema(BaseModel):
    fullname: str
    username: str
    tenant_id: str
    password: str

    @field_validator("tenant_id")
    def tenant_id_must_be_number(cls, v):
        if not v.isnumeric():
            raise ValueError("Must contain number only")
        return v
