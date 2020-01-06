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
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, datetime.timedelta):
            return str(obj.total_seconds())
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, bytes):
            return obj.decode()
        if hasattr(obj, 'tolist'):
            return obj.tolist()
        if hasattr(obj, '__getitem__'):
            cls = (list if isinstance(obj, (list, tuple)) else dict)
            try:
                return cls(obj)
            except Exception:
                pass
        if hasattr(obj, '__iter__'):
            return tuple(item for item in obj)
        return super().default(obj)
