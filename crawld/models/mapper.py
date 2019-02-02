import bs4
import requests

from crawld.models import ParsingError
from crawld.models.utils import fields


class MapperMeta(type):
    def __init__(cls, name, bases, dct):
        if bases != (object,) and not dct.get('__abstract__', False):
            if dct.get('__object_class__') is None:
                raise ValueError(f'Model \'{name}\' doesn\'t have an __object_class__')

            dct['__object_class__'].__mapper__ = cls

        super().__init__(name, bases, dct)


class Mapper(object, metaclass=MapperMeta):
    __page_url__ = ''
    __object_class__ = None

    def __init__(self):
        self.fields = []

        for field_name, field in fields(self.__class__.__dict__):
            self.fields.append(field)

            field.bind(
                name=field_name,
                mapper=self
            )

    def get_page_url(self, **context):
        return self.__page_url__.format(**context)

    def fetch_page(self, page_url, **context):
        cookies = context.get('cookies', {})
        page_text = requests.get(page_url, cookies=cookies).text
        soup = bs4.BeautifulSoup(page_text, features='lxml')
        return soup, context

    def parse_data(self, soup, **context):
        objects = []
        for dom_node in self.get_dom_node_list(soup, **context):
            obj = {}
            for field in self.fields:
                value = field.parse_wrapper(
                    data=dom_node,
                    **context
                )
                if not value and field.required:
                    raise ParsingError(field.field_name, 'this field is required')
                obj[field.name] = value

            objects.append(obj)

        return [self.__object_class__(**values) for values in objects]

    def fetch_and_parse(self, **context):
        soup, context = self.fetch_page(
            page_url=self.get_page_url(**context),
            **context
        )
        return self.parse_data(
            soup=soup,
            **context
        )

    def get_dom_node_list(self, soup, **context):
        return [soup]
