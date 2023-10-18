def from_spec(spec, kwargs=None):
        """
        Creates a preprocessing stack from a specification dict.
        """
        if isinstance(spec, dict):
            spec = [spec]

        stack = PreprocessorStack()
        for preprocessor_spec in spec:
            # need to deep copy, otherwise will add first processors spec_ to kwargs to second processor
            preprocessor_kwargs = copy.deepcopy(kwargs)
            preprocessor = util.get_object(
                obj=preprocessor_spec,
                predefined_objects=tensorforce.core.preprocessors.preprocessors,
                kwargs=preprocessor_kwargs
            )
            assert isinstance(preprocessor, Preprocessor)
            stack.preprocessors.append(preprocessor)

        return stack