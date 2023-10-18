def _isobject(self, name, exist):
        """Test whether the name is an object."""
        if exist in [2, 5]:
            return False
        cmd = 'isobject(%s)' % name
        resp = self._engine.eval(cmd, silent=True).strip()
        return resp == 'ans =  1'