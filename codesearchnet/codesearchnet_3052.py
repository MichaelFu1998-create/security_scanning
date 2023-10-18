def send(self, str, end='\n'):
        """Sends a line to std_in."""
        return self._process.stdin.write(str+end)