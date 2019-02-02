from crawld.models import ParsingError


def operator(name, *args, **kwargs):
    def wrapper(fn):
        fn.name = name
        fn.args = args
        fn.kwargs = kwargs
        fn.__repr__ = lambda self: f'<Operator {name}({args}, {kwargs})>'
        return fn
    return wrapper


class Pipe:
    def __init__(self, operators=None, required=True):
        if not operators:
            operators = []
        self.operators = operators
        self.name = None
        self.mapper = None

        self.required = required

    def select(self, selector, **options):
        @operator('select', selector)
        def wrapper(data, **kwargs):
            def mapping(value):
                return value.select(selector)
            return self._apply(mapping, data, **options)
        self.operators.append(wrapper)
        return self

    def attribute(self, name, **options):
        @operator('attribute', name)
        def wrapper(data, **kwargs):
            def mapping(value):
                return value[name]
            return self._apply(mapping, data, **options)
        self.operators.append(wrapper)
        return self

    def text(self, **options):
        @operator('text')
        def wrapper(data, **kwargs):
            def mapping(value):
                return value.text
            return self._apply(mapping, data, **options)
        self.operators.append(wrapper)
        return self

    def context_attribute(self, name):
        @operator('context_attribute', name)
        def wrapper(data, **kwargs):
            return kwargs[name]
        self.operators.append(wrapper)
        return self

    def function(self, fn, **options):
        @operator('function', fn)
        def wrapper(data, **kwargs):
            def mapping(value):
                return fn(value, **kwargs)
            return self._apply(mapping, data, **options)
        self.operators.append(wrapper)
        return self

    def spawn(self, mapper, **options):
        @operator('spawn', mapper)
        def wrapper(data, **kwargs):
            def mapping(value):
                return mapper().parse_data(soup=value, **kwargs)
            return self._apply(mapping, data, **options)
        self.operators.append(wrapper)
        return self

    def clone(self):
        return Pipe(self.operators, self.required)

    # region maintenance functions

    def parse(self, data, **kwargs):
        value = data
        for op in self.operators:
            value = op(value, **kwargs)
        return value

    def parse_wrapper(self, data, **kwargs):
        try:
            return self.parse(data, **kwargs)
        except Exception as e:
            if self.required:
                raise ParsingError(self.name, str(e))

    def bind(self, name, mapper):
        self.name = name
        self.mapper = mapper

    def _apply(self, mapping, data, **options):
        many = options.get('many', False)
        first = options.get('first', False)

        def arg_mapping(x):
            if first:
                x = x[0]
            return x

        if many:
            return [mapping(arg_mapping(x)) for x in data]
        else:
            return mapping(arg_mapping(data))

    def __repr__(self):
        pipeline = []
        for op in self.operators:
            op_args = [
                *(str(x) for x in op.args),
                *(f'{k}={v}' for k, v in op.kwargs.items())
            ]
            op_args = ', '.join(op_args)
            pipeline.append(f'{op.name}({op_args})')

        pipeline = ', '.join(pipeline)

        return f'<Pipe [{pipeline}]>'


def pipe(operators=None, **kwargs):
    return Pipe(operators, **kwargs)
