def debug(self, builddir, program):
        ''' Launch a debugger for the specified program. Uses the `debug`
            script if specified by the target, falls back to the `debug` and
            `debugServer` commands if not. `program` is inserted into the
            $program variable in commands.
        '''
        try:
            signal.signal(signal.SIGINT, _ignoreSignal);
            if self.getScript('debug') is not None:
                return self._debugWithScript(builddir, program)
            elif 'debug' in self.description:
                logger.warning(
                    'target %s provides deprecated debug property. It should '+
                    'provide script.debug instead.', self.getName()

                )
                return self._debugDeprecated(builddir, program)
            else:
                return "Target %s does not specify debug commands" % self
        finally:
            # clear the sigint handler
            signal.signal(signal.SIGINT, signal.SIG_DFL);