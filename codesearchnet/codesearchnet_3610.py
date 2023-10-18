def current_vm(self):
        """current vm"""
        try:
            _, _, _, _, vm = self._callstack[-1]
            return vm
        except IndexError:
            return None