class EntityState:
    '''
    obj = EntityState(
        [value, code, name],
        [value, code, name],
        [value, code, name],
    )

    obj.code -> value
    obj[name] -> value
    obj.items() -> (
                    (value, name),
                    (value, name),
                    (value, name),
                    )

    '''

    def __init__(self, *args):
        self._items = args

    def __getattr__(self, item):
        if isinstance(item, str):
            for value, code, name in self._items:
                if code == item:
                    return value

        super(EntityState, self).__getattribute__(item)

    def __getitem__(self, item):
        if isinstance(item, int):
            for value, code, name in self._items:
                if value == item:
                    return name

        if isinstance(item, str):
            for value, code, name in self._items:
                if name == item:
                    return value

        raise KeyError()

    def items(self):
        return [(value, name) for value, code, name in self._items]
