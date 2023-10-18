def __init(self,code):
        """Initialize a `MucStatus` element from a status code.

        :Parameters:
            - `code`: the status code.
        :Types:
            - `code`: `int`
        """
        code=int(code)
        if code<0 or code>999:
            raise ValueError("Bad status code")
        self.code=code