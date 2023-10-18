def url_correct(self, point, auth=None, export=None):
        '''
        Returns a Corrected URL to be used for a Request
        as per the REST API.
        '''
        newUrl = self.__url + point + '.json'
        if auth or export:
            newUrl += "?"
        if auth:
            newUrl += ("auth=" + auth)
        if export:
            if not newUrl.endswith('?'):
                newUrl += "&"
            newUrl += "format=export"
        return newUrl