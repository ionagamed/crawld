class ParsingError(Exception):
    def __init__(self, field, message):
        self.field = field
        self.message = message

    def __str__(self):
        return f'Error parsing field \'{self.field}\' - {self.message}'
