from marshmallow import Schema, fields


class EventSchema(Schema):
    """Serializer for events."""

    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(format="%Y-%m-%d")
    data = fields.Raw()
