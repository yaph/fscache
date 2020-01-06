# -*- coding: utf-8 -*-
"""Helper class for encoding data."""

import datetime
import decimal
import json
import uuid


class JSONEncoder(json.JSONEncoder):
    """
    Source https://github.com/encode/django-rest-framework/blob/master/rest_framework/utils/encoders.py
    JSONEncoder that encodes date/timedelta, decimal types, generators and other basic python objects.
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            representation = obj.isoformat()
            if representation.endswith('+00:00'):
                representation = representation[:-6] + 'Z'
            return representation
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return str(obj.total_seconds())
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, bytes):
            return obj.decode()
        elif hasattr(obj, 'tolist'):
            return obj.tolist()
        elif hasattr(obj, '__getitem__'):
            cls = (list if isinstance(obj, (list, tuple)) else dict)
            try:
                return cls(obj)
            except Exception:
                pass
        elif hasattr(obj, '__iter__'):
            return tuple(item for item in obj)
        return super().default(obj)
