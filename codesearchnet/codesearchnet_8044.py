def apply(self, **kwexpr):
        """
        Specify one or more projection expressions to add to each result

        ### Parameters

        - **kwexpr**: One or more key-value pairs for a projection. The key is
            the alias for the projection, and the value is the projection
            expression itself, for example `apply(square_root="sqrt(@foo)")`
        """
        for alias, expr in kwexpr.items():
            self._projections.append([alias, expr])

        return self