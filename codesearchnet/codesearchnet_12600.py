def run(self, *args, **kw):
        """
        Runs the current operator with the subject arguments to test.

        This method is implemented by matchers only.
        """
        log.debug('[operator] run "{}" with arguments: {}'.format(
            self.__class__.__name__, args
        ))

        if self.kind == OperatorTypes.ATTRIBUTE:
            return self.match(self.ctx)
        else:
            return self.run_matcher(*args, **kw)