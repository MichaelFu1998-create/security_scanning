def isMine(self, scriptname):
        """Primitive queuing system detection; only looks at suffix at the moment."""
        suffix = os.path.splitext(scriptname)[1].lower()
        if suffix.startswith('.'):
            suffix = suffix[1:]
        return self.suffix == suffix