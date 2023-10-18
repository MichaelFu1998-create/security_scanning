def callprop(self, prop, *args):
        '''Call a property prop as a method (this will be self).

        NOTE: dont pass this and arguments here, these will be added
        automatically!'''
        if not isinstance(prop, basestring):
            prop = prop.to_string().value
        cand = self.get(prop)
        if not cand.is_callable():
            raise MakeError('TypeError',
                            '%s is not a function' % cand.typeof())
        return cand.call(self, args)