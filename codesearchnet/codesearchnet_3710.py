def _convert_pagenum(self, kwargs):
        """
        Convert next and previous from URLs to integers
        """
        for key in ('next', 'previous'):
            if not kwargs.get(key):
                continue
            match = re.search(r'page=(?P<num>[\d]+)', kwargs[key])
            if match is None and key == 'previous':
                kwargs[key] = 1
                continue
            kwargs[key] = int(match.groupdict()['num'])