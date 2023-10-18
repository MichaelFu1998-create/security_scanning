def process(self, tensor):
        """
        Process state.

        Args:
            tensor: tensor to process

        Returns: processed state

        """
        for processor in self.preprocessors:
            tensor = processor.process(tensor=tensor)
        return tensor