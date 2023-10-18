def set_callbacks(self, **kwargs):
        ''' Set callbacks for input events '''
        for name in self.SUPPORTED_CALLBACKS:
            func = kwargs.get(name, getattr(self, name))
            setattr(self, name, func)