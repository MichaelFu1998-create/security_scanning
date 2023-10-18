def reset(self):
        """
        Calls `reset` on all our Preprocessor objects.

        Returns:
            A list of tensors to be fetched.
        """
        fetches = []
        for processor in self.preprocessors:
            fetches.extend(processor.reset() or [])
        return fetches