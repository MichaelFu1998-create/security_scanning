def reviews(self, packageName, filterByDevice=False, sort=2,
                nb_results=None, offset=None):
        """Browse reviews for an application

        Args:
            packageName (str): app unique ID.
            filterByDevice (bool): filter results for current device
            sort (int): sorting criteria (values are unknown)
            nb_results (int): max number of reviews to return
            offset (int): return reviews starting from an offset value

        Returns:
            dict object containing all the protobuf data returned from
            the api
        """
        # TODO: select the number of reviews to return
        path = REVIEWS_URL + "?doc={}&sort={}".format(requests.utils.quote(packageName), sort)
        if nb_results is not None:
            path += "&n={}".format(nb_results)
        if offset is not None:
            path += "&o={}".format(offset)
        if filterByDevice:
            path += "&dfil=1"
        data = self.executeRequestApi2(path)
        output = []
        for review in data.payload.reviewResponse.getResponse.review:
            output.append(utils.parseProtobufObj(review))
        return output