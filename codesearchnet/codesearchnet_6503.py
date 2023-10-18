def details(self, packageName):
        """Get app details from a package name.

        packageName is the app unique ID (usually starting with 'com.')."""
        path = DETAILS_URL + "?doc={}".format(requests.utils.quote(packageName))
        data = self.executeRequestApi2(path)
        return utils.parseProtobufObj(data.payload.detailsResponse.docV2)