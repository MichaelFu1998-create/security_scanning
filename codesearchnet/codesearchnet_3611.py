def current_transaction(self):
        """current tx"""
        try:
            tx, _, _, _, _ = self._callstack[-1]
            if tx.result is not None:
                #That tx finished. No current tx.
                return None
            return tx
        except IndexError:
            return None