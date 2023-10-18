def objectid_valid(i):
        """ Test if a string looks like a regular object id of the
            form:::

               xxxx.yyyyy.zzzz

            with those being numbers.
        """
        if "." not in i:
            return False
        parts = i.split(".")
        if len(parts) == 3:
            try:
                [int(x) for x in parts]
                return True
            except Exception:
                pass
            return False