def _make(cls, iterable, new=tuple.__new__, len=len):
        'Make a new Match object from a sequence or iterable'
        result = new(cls, iterable)
        if len(result) != 3:
            raise TypeError('Expected 3 arguments, got %d' % len(result))
        return result