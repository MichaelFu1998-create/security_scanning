def _interrupt(self, uc, number, data):
        """
        Handle software interrupt (SVC/INT)
        """

        from ..native.cpu.abstractcpu import Interruption  # prevent circular imports
        self._to_raise = Interruption(number)
        return True