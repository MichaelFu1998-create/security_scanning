def emulate(self, instruction):
        """
        Wrapper that runs the _step function in a loop while handling exceptions
        """

        # The emulation might restart if Unicorn needs to bring in a memory map
        # or bring a value from Manticore state.
        while True:

            # Try emulation
            self._should_try_again = False
            self._to_raise = None

            self._step(instruction)

            if not self._should_try_again:
                break