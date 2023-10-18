def get_all_params(self, session=None):
        """Return the parameters in a list of array."""
        _params = []
        for p in self.all_params:
            if session is None:
                _params.append(p.eval())
            else:
                _params.append(session.run(p))
        return _params