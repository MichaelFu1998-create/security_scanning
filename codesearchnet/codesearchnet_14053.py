def _mouse_pointer_moved(self, x, y):
        '''GUI callback for mouse moved'''
        self._namespace['MOUSEX'] = x
        self._namespace['MOUSEY'] = y