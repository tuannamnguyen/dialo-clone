from src.db_instance import instance
from umongo import Document, fields

@instance.register
class QueueModel(Document):
    queue_id = fields.StringField(unique=True, allow_none=True)
    list_extension_id = fields.ListField(fields.StringField(), allow_none=True),
    description = fields.StringField(allow_none=True)
    tenant = fields.StringField(allow_none=True)

    class Meta: 
        collection_name = "Queue"