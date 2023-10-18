def _get_backend_parameters(self):
        """
        Gets the pyqode backend parameters (interpreter and script).
        """
        frozen = hasattr(sys, 'frozen')
        interpreter = Settings().interpreter
        if frozen:
            interpreter = None
        pyserver = server.__file__ if interpreter is not None else 'server.exe'
        args = []
        return interpreter, pyserver, args