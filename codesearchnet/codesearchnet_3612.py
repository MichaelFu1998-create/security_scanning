def current_human_transaction(self):
        """Current ongoing human transaction"""
        try:
            tx, _, _, _, _ = self._callstack[0]
            if tx.result is not None:
                #That tx finished. No current tx.
                return None
            assert tx.depth == 0
            return tx
        except IndexError:
            return None