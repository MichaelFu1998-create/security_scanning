def bulkDetails(self, packageNames):
        """Get several apps details from a list of package names.

        This is much more efficient than calling N times details() since it
        requires only one request. If an item is not found it returns an empty object
        instead of throwing a RequestError('Item not found') like the details() function

        Args:
            packageNames (list): a list of app IDs (usually starting with 'com.').

        Returns:
            a list of dictionaries containing docv2 data, or None
            if the app doesn't exist"""

        params = {'au': '1'}
        req = googleplay_pb2.BulkDetailsRequest()
        req.docid.extend(packageNames)
        data = req.SerializeToString()
        message = self.executeRequestApi2(BULK_URL,
                                          post_data=data.decode("utf-8"),
                                          content_type=CONTENT_TYPE_PROTO,
                                          params=params)
        response = message.payload.bulkDetailsResponse
        return [None if not utils.hasDoc(entry) else
                utils.parseProtobufObj(entry.doc)
                for entry in response.entry]