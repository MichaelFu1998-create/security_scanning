def processed_shape(self, shape):
        """
        Shape of preprocessed state given original shape.

        Args:
            shape: original state shape

        Returns: processed state shape
        """
        for processor in self.preprocessors:
            shape = processor.processed_shape(shape=shape)
        return shape