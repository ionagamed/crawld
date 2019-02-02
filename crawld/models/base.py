class Model(object):
    __mapper__ = None

    @classmethod
    def get_one(cls, **context):
        try:
            return cls.__mapper__().fetch_and_parse(**context)[0]
        except IndexError:
            return None

    @classmethod
    def get_many(cls, **context):
        return cls.__mapper__().fetch_and_parse(**context)
