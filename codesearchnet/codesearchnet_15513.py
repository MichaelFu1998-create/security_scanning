def isstring(self, string, *args):
        """Is string
        args:
            string (str): match
        returns:
            bool
        """
        regex = re.compile(r'\'[^\']*\'|"[^"]*"')
        return regex.match(string)