def walk(self, maxresults=100, maxdepth=None):
        """Walk the object tree, ignoring duplicates and circular refs."""
        log.debug("step")
        self.seen = {}
        self.ignore(self, self.__dict__, self.obj, self.seen, self._ignore)

        # Ignore the calling frame, its builtins, globals and locals
        self.ignore_caller()
        self.maxdepth = maxdepth
        count = 0
        log.debug("will iterate results")
        for result in self._gen(self.obj):
            log.debug("will yeld")
            yield result
            count += 1
            if maxresults and count >= maxresults:
                yield 0, 0, "==== Max results reached ===="
                return