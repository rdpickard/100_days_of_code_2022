import sqlalchemy
import sqlalchemy.ext.mutable
import json


class MutableDict(sqlalchemy.ext.mutable.Mutable, dict):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/mutable.html

    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return sqlalchemy.ext.mutable.Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


class JSONEncodedDict(sqlalchemy.types.TypeDecorator):
    # https://docs.sqlalchemy.org/en/14/core/custom_types.html#marshal-json-strings

    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict(255)

    """

    impl = sqlalchemy.types.VARCHAR

    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


json_type = MutableDict.as_mutable(JSONEncodedDict)