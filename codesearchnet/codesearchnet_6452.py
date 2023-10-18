def find_service(self, uuid):
        """Return the first child service found that has the specified
        UUID.  Will return None if no service that matches is found.
        """
        for service in self.list_services():
            if service.uuid == uuid:
                return service
        return None