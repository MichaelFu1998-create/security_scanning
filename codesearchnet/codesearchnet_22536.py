def parse(self, string):
        """
        Parse runtime path representation to list.

        :param string string: runtime path string
        :return: list of runtime paths
        :rtype: list of string
        """
        var, eq, values = string.strip().partition('=')
        assert var == 'runtimepath'
        assert eq == '='
        return values.split(',')