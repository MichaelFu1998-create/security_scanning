def get_version(self):
        '''obtain the version or just 2.2.x if < 2.3.x
        Raises:
            FailedRequestError: If the request fails.
        '''
        if self._version:
            return self._version
        url = "{}/about/version.xml".format(self.service_url)
        resp = self.http_request(url)
        version = None
        if resp.status_code == 200:
            dom = XML(resp.content)
            resources = dom.findall("resource")
            for resource in resources:
                if resource.attrib["name"] == "GeoServer":
                    try:
                        version = resource.find("Version").text
                        break
                    except AttributeError:
                        pass

        # This will raise an exception if the catalog is not available
        # If the catalog is available but could not return version information,
        # it is an old version that does not support that
        if version is None:
            # just to inform that version < 2.3.x
            version = "2.2.x"
        self._version = version
        return version