def get_object(self, name):
        """Retrieve an object by its absolute name."""

        parts = name.split(".")

        model_name = parts.pop(0)
        return self.models[model_name].get_object(".".join(parts))