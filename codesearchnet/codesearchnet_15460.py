def press_key(self, key, mode=0):
        '''
        modes:
            0 -> simple press
            1 -> long press
            2 -> release after long press
        '''
        if isinstance(key, str):
            assert key in KEYS, 'No such key: {}'.format(key)
            key = KEYS[key]
        _LOGGER.info('Press key %s', self.__get_key_name(key))
        return self.rq('01', OrderedDict([('key', key), ('mode', mode)]))