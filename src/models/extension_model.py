from src.db_instance import instance
from umongo import Document, fields

@instance.register
class ExtensionModel(Document):
    extension_id = fields.StringField(unique=True, allow_none=True)
    list_queue_id = fields.ListField(fields.StringField(), allow_none=True)
    agent = fields.StringField(unique=True, allow_none=True)
    status = fields.StringField(allow_none=True)
    description = fields.StringField(allow_none=True)
    tenant = fields.StringField(allow_none=True)

    class Meta:
        collection_name = "Extensions"