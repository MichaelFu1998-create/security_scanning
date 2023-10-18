def _recv(self) -> str:
        """Reads the response from the solver"""
        buf, left, right = self.__readline_and_count()
        bufl = [buf]

        while left != right:
            buf, l, r = self.__readline_and_count()
            bufl.append(buf)
            left += l
            right += r

        buf = ''.join(bufl).strip()

        logger.debug('<%s', buf)
        if '(error' in bufl[0]:
            raise Exception(f"Error in smtlib: {bufl[0]}")
        return buf