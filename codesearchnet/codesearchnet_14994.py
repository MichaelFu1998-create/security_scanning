def save_service(self, service, overwrite=True):
        """
        Store an OWS service in database.
        """
        name = namesgenerator.get_sane_name(service.name)
        if not name:
            name = namesgenerator.get_random_name()
            if name in self.name_index:
                name = namesgenerator.get_random_name(retry=True)
        # check if service is already registered
        if name in self.name_index:
            if overwrite:
                self._delete(name=name)
            else:
                raise Exception("service name already registered.")
        self._insert(Service(
            name=name,
            url=baseurl(service.url),
            type=service.type,
            purl=service.purl,
            public=service.public,
            auth=service.auth,
            verify=service.verify))
        return self.fetch_by_name(name=name)