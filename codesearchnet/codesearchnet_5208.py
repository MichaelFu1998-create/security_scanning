def _is_string(value):
        """
            Checks if the value provided is a string (True) or not integer
            (False) or something else (None).
        """
        if type(value) in [type(u''), type('')]:
            return True
        elif type(value) in [int, type(2 ** 64)]:
            return False
        else:
            return None