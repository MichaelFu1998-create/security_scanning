def settings(self, **kwargs):
        '''
        Pass a load of settings into the canvas
        '''
        for k, v in kwargs.items():
            setattr(self, k, v)