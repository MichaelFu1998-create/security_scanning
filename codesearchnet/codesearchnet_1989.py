def index(self, value):
        '''S.index(value) -> integer -- return first index of value.
           Raises ValueError if the value is not present.
        '''
        for i, v in enumerate(self):
            if v == value:
                return i
        raise ValueError