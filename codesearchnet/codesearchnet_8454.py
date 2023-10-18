def __parse_parms(self):
        """Translate dict parameters to string"""

        args = list()
        for key, val in self.__parm.items():
            key = key.replace("FIO_", "").lower()

            if key == "runtime":
                args.append("--time_based")

            if val is None:
                args.append("--%s" % key)
            else:
                args.append("--%s=%s" % (key, val))
        return args