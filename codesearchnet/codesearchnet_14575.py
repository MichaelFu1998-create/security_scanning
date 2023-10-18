def _underscore_to_camelcase(value):
        """
        Convert Python snake case back to mixed case.
        """
        def camelcase():
            yield str.lower
            while True:
                yield str.capitalize

        c = camelcase()
        return "".join(next(c)(x) if x else '_' for x in value.split("_"))