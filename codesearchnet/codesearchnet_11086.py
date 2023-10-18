def create_effect(self, label: str, name: str, *args, **kwargs) -> Effect:
        """
        Create an effect instance adding it to the internal effects dictionary using the label as key.

        Args:
            label (str): The unique label for the effect instance
            name (str): Name or full python path to the effect class we want to instantiate
            args: Positional arguments to the effect initializer
            kwargs: Keyword arguments to the effect initializer

        Returns:
            The newly created Effect instance
        """
        effect_cls = effects.find_effect_class(name)
        effect = effect_cls(*args, **kwargs)
        effect._label = label

        if label in self._effects:
            raise ValueError("An effect with label '{}' already exists".format(label))

        self._effects[label] = effect

        return effect