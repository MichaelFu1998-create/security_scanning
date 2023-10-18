def save_service(self, service, overwrite=True):
        """
        Stores an OWS service in mongodb.
        """
        name = namesgenerator.get_sane_name(service.name)
        if not name:
            name = namesgenerator.get_random_name()
            if self.collection.count_documents({'name': name}) > 0:
                name = namesgenerator.get_random_name(retry=True)
        # check if service is already registered
        if self.collection.count_documents({'name': name}) > 0:
            if overwrite:
                self.collection.delete_one({'name': name})
            else:
                raise Exception("service name already registered.")
        self.collection.insert_one(Service(
            name=name,
            url=baseurl(service.url),
            type=service.type,
            purl=service.purl,
            public=service.public,
            auth=service.auth,
            verify=service.verify))
        return self.fetch_by_name(name=name)