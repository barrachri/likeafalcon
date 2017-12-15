
from marshmallow import Schema, fields, post_dump

class EventSchema(Schema):
    """Serializer for Probe model."""

    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(format="%Y-%m-%d")
    data = fields.Raw()
