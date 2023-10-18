def fmt(self, fills):
        """ Format node
        args:
            fills (dict): replacements
        returns:
            str
        """
        f = "%(tab)s%(property)s:%(ws)s%(style)s%(important)s;%(nl)s"
        imp = ' !important' if self.important else ''
        if fills['nl']:
            self.parsed = [
                ',%s' % fills['ws'] if p == ',' else p for p in self.parsed
            ]
        style = ''.join([
            p.fmt(fills) if hasattr(p, 'fmt') else str(p) for p in self.parsed
        ])
        # IE cannot handle no space after url()
        style = re.sub("(url\([^\)]*\))([^\s,])", "\\1 \\2", style)
        fills.update({
            'property': self.property,
            'style': style.strip(),
            'important': imp
        })
        return f % fills