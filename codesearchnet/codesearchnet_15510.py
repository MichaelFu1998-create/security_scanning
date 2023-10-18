def sformat(self, string, *args):
        """ String format.
        args:
            string (str): string to format
            args (list): format options
        returns:
            str
        """
        format = string
        items = []
        m = re.findall('(%[asdA])', format)
        if m and not args:
            raise SyntaxError('Not enough arguments...')
        i = 0
        for n in m:
            v = {
                '%A': urlquote,
                '%s': utility.destring,
            }.get(n, str)(args[i])
            items.append(v)
            i += 1
        format = format.replace('%A', '%s')
        format = format.replace('%d', '%s')
        return format % tuple(items)