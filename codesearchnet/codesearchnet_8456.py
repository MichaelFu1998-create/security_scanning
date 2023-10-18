def get_parm(self, key):
        """Get parameter of FIO"""

        if key in self.__parm.keys():
            return self.__parm[key]

        return None