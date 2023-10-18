def fmt(self, fills):
        """Format identifier
        args:
            fills (dict): replacements
        returns:
            str (CSS)
        """
        name = ',$$'.join(''.join(p).strip() for p in self.parsed)
        name = re.sub('\?(.)\?', '%(ws)s\\1%(ws)s', name) % fills
        return name.replace('$$', fills['nl']).replace('  ', ' ')