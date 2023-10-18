def run(self):
        """
        Create a unique instance of Octave and verify namespace uniqueness.

        Raises
        ======
        Oct2PyError
            If the thread does not sucessfully demonstrate independence

        """
        octave = Oct2Py()
        # write the same variable name in each thread and read it back
        octave.push('name', self.getName())
        name = octave.pull('name')
        now = datetime.datetime.now()
        print("{0} got '{1}' at {2}".format(self.getName(), name, now))
        octave.exit()
        try:
            assert self.getName() == name
        except AssertionError:  # pragma: no cover
            raise Oct2PyError('Thread collision detected')
        return