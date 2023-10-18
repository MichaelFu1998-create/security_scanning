def isnumber(self, string, *args):
        """Is number
        args:
            string (str): match
        returns:
            bool
        """
        try:
            n, u = utility.analyze_number(string)
        except SyntaxError:
            return False
        return True