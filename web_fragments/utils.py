"""
Useful utilities.
"""

import json
import decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse


class EDXJSONEncoder(DjangoJSONEncoder):
    """
    Encoder for Decimal object, other objects will be encoded as per DjangoJSONEncoder default implementation.

    NOTE:
        Please see https://docs.djangoproject.com/en/1.8/releases/1.5/#system-version-of-simplejson-no-longer-used
        DjangoJSONEncoder will now use the Python's json module but Python's json module don't know about how to
        encode Decimal object, so as per default implementation Decimal objects will be encoded to `str` which we don't
        want and also this is different from Django 1.4, In Django 1.4 if Decimal object has zeros after the decimal
        point then object will be serialized as `int` else `float`, so we are keeping this behavior.
    """
    def default(self, o):  # pylint: disable=method-hidden
        """
        Encode Decimal objects. If decimal object has zeros after the
        decimal point then object will be serialized as `int` else `float`
        """
        if isinstance(o, decimal.Decimal):
            if o == o.to_integral():
                return int(o)
            return float(o)
        else:
            return super(EDXJSONEncoder, self).default(o)


class JsonResponse(HttpResponse):
    """
    Django HttpResponse subclass that has sensible defaults for outputting JSON.
    """
    def __init__(self, resp_obj=None, status=None, encoder=EDXJSONEncoder,
                 *args, **kwargs):
        if resp_obj in (None, ""):
            content = ""
            status = status or 204
        elif isinstance(resp_obj, QuerySet):
            content = serialize('json', resp_obj)
        else:
            content = json.dumps(resp_obj, cls=encoder, indent=2, ensure_ascii=True)
        kwargs.setdefault("content_type", "application/json")
        if status:
            kwargs["status"] = status
        super(JsonResponse, self).__init__(content, *args, **kwargs)


