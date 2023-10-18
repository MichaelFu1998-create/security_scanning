def set_password(self, service, username, password):
        """Set password for the username of the service
        """
        collection = self.get_preferred_collection()
        attributes = {
            "application": self.appid,
            "service": service,
            "username": username
        }
        label = "Password for '{}' on '{}'".format(username, service)
        collection.create_item(label, attributes, password, replace=True)