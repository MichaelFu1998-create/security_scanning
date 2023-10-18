def capture_bash(self):
        """
        Context manager that hides the command prefix and activates dryrun to capture all following task commands to their equivalent Bash outputs.
        """
        class Capture(object):

            def __init__(self, satchel):
                self.satchel = satchel
                self._dryrun = self.satchel.dryrun
                self.satchel.dryrun = 1
                begincap()
                self._stdout = sys.stdout
                self._stderr = sys.stderr
                self.stdout = sys.stdout = StringIO()
                self.stderr = sys.stderr = StringIO()

            def __enter__(self):
                return self

            def __exit__(self, type, value, traceback): # pylint: disable=redefined-builtin
                endcap()
                self.satchel.dryrun = self._dryrun
                sys.stdout = self._stdout
                sys.stderr = self._stderr

        return Capture(self)