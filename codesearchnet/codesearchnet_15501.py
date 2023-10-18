def preprocess(self, style):
        """Hackish preprocessing from font shorthand tags.
        Skips expression parse on certain tags.
        args:
            style (list): .
        returns:
            list
        """
        if self.property == 'font':
            style = [
                ''.join(u.expression()) if hasattr(u, 'expression') else u
                for u in style
            ]
        else:
            style = [(u, ' ') if hasattr(u, 'expression') else u
                     for u in style]
        return style