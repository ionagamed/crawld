class Manager(object):
    list = None
    detail = None

    @classmethod
    def get_list(cls, **context):
        return cls.list.get_many(**context)

    @classmethod
    def get_detail(cls, **context):
        return cls.detail.get_one(**context)
