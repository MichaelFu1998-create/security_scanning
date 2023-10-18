def save(self, obj, content_type="application/xml"):
        """
        saves an object to the REST service
        gets the object's REST location and the data from the object,
        then POSTS the request.
        """
        rest_url = obj.href
        data = obj.message()

        headers = {
            "Content-type": content_type,
            "Accept": content_type
        }

        logger.debug("{} {}".format(obj.save_method, obj.href))
        resp = self.http_request(rest_url, method=obj.save_method.lower(), data=data, headers=headers)

        if resp.status_code not in (200, 201):
            raise FailedRequestError('Failed to save to Geoserver catalog: {}, {}'.format(resp.status_code, resp.text))

        self._cache.clear()
        return resp