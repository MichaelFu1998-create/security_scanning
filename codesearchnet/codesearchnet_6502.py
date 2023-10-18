def search(self, query):
        """ Search the play store for an app.

        nb_result (int): is the maximum number of result to be returned

        offset (int): is used to take result starting from an index.
        """
        if self.authSubToken is None:
            raise LoginError("You need to login before executing any request")

        path = SEARCH_URL + "?c=3&q={}".format(requests.utils.quote(query))
        # FIXME: not sure if this toc call should be here
        self.toc()
        data = self.executeRequestApi2(path)
        if utils.hasPrefetch(data):
            response = data.preFetch[0].response
        else:
            response = data
        resIterator = response.payload.listResponse.doc
        return list(map(utils.parseProtobufObj, resIterator))