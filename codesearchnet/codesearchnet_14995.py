def list_services(self):
        """
        Lists all services in memory storage.
        """
        my_services = []
        for service in self.name_index.values():
            my_services.append(Service(service))
        return my_services