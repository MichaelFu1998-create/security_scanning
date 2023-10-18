def get_orthographies(self, _library=library):
        ''' Returns list of CharsetInfo about supported orthographies '''
        results = []
        for charset in _library.charsets:
            if self._charsets:
                cn = getattr(charset, 'common_name', False)
                abbr = getattr(charset, 'abbreviation', False)
                nn = getattr(charset, 'short_name', False)
                naive = getattr(charset, 'native_name', False)

                if cn and cn.lower() in self._charsets:
                    results.append(charset)

                elif nn and nn.lower() in self._charsets:
                    results.append(charset)

                elif naive and naive.lower() in self._charsets:
                    results.append(charset)

                elif abbr and abbr.lower() in self._charsets:
                    results.append(charset)
            else:
                results.append(charset)

        for result in results:
            yield CharsetInfo(self, result)