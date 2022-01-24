class MissingArgument(Exception):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return f'Missing argument "{self.arg}" by running the script.'
