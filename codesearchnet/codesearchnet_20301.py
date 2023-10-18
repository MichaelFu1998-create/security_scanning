def pip_r(self, requirements, raise_on_error=True):
        """
        Install all requirements contained in the given file path
        Waits for command to finish.

        Parameters
        ----------
        requirements: str
            Path to requirements.txt
        raise_on_error: bool, default True
            If True then raise ValueError if stderr is not empty
        """
        cmd = "pip install -r %s" % requirements
        return self.wait(cmd, raise_on_error=raise_on_error)