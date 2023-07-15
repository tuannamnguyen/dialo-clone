from umongo import Document, fields

from src.db_instance import instance


@instance.register
class User(Document):
    fullname = fields.StringField(required=True)
    username = fields.StringField(unique=True, required=True)
    tenant_id = fields.StringField(required=True)
    password = fields.StringField(required=True)

    class Meta:
        collection_name = "users"