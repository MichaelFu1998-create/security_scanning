def _key_pressed(self, key, keycode):
        '''GUI callback for key pressed'''
        self._namespace['key'] = key
        self._namespace['keycode'] = keycode
        self._namespace['keydown'] = True