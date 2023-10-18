def register(self, model_cls):
        """Register model(s) with app"""
        assert issubclass(model_cls, peewee.Model)
        assert not hasattr(model_cls._meta, 'database_manager')
        if model_cls in self:
            raise RuntimeError("Model already registered")
        self.append(model_cls)
        model_cls._meta.database = self.dbm
        return model_cls