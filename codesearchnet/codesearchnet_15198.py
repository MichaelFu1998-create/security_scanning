def unfix(self, param):
        """
        Enable parameter optimization.

        Parameters
        ----------
        param : str
            Possible values are ``"delta"``, ``"beta"``, and ``"scale"``.
        """
        if param == "delta":
            self._unfix("logistic")
        else:
            self._fix[param] = False