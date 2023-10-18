def fix(self, param):
        """
        Disable parameter optimization.

        Parameters
        ----------
        param : str
            Possible values are ``"delta"``, ``"beta"``, and ``"scale"``.
        """
        if param == "delta":
            super()._fix("logistic")
        else:
            self._fix[param] = True