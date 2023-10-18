def update(self, **kwargs):
        """Override settings values"""
        for name, value in kwargs.items():
            setattr(self, name, value)