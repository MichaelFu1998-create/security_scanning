def fmt(self, fills):
        """Format block (CSS)
        args:
            fills (dict): Fill elements
        returns:
            str (CSS)
        """
        f = "%(identifier)s%(ws)s{%(nl)s%(proplist)s}%(eb)s"
        out = []
        name = self.name.fmt(fills)
        if self.parsed and any(
                p for p in self.parsed
                if str(type(p)) != "<class 'lesscpy.plib.variable.Variable'>"):
            fills.update({
                'identifier':
                name,
                'proplist':
                ''.join([p.fmt(fills) for p in self.parsed if p]),
            })
            out.append(f % fills)
        if hasattr(self, 'inner'):
            if self.name.subparse and len(self.inner) > 0:  # @media
                inner = ''.join([p.fmt(fills) for p in self.inner])
                inner = inner.replace(fills['nl'],
                                      fills['nl'] + fills['tab']).rstrip(
                                          fills['tab'])
                if not fills['nl']:
                    inner = inner.strip()
                fills.update({
                    'identifier': name,
                    'proplist': fills['tab'] + inner
                })
                out.append(f % fills)
            else:
                out.append(''.join([p.fmt(fills) for p in self.inner]))
        return ''.join(out)