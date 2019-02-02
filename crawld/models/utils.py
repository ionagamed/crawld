from crawld.models.pipes import Pipe


def fields(dct):
    for key, value in dct.items():
        if isinstance(value, Pipe):
            yield key, value


def slice_into_objects(dct):
    object_count = len(next(iter(dct.values())))
    objects = [{} for x in range(object_count)]

    for key, values in dct.items():
        if not isinstance(values, list):
            raise TypeError
        if len(values) != object_count:
            raise ValueError

        for i, value in enumerate(values):
            objects[i][key] = value

    return objects
