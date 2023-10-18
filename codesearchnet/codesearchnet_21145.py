def add(self, *names):
        '''Returns back a class decorator that enables registering Blox to this factory'''
        def decorator(blok):
            for name in names or (blok.__name__, ):
                self[name] = blok
            return blok
        return decorator