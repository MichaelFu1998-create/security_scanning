def register(self, model):
        """Register a model in self."""
        self.models[model._meta.table_name] = model
        model._meta.database = self.database
        return model