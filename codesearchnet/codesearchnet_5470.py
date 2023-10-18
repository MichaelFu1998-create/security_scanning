def container_id(self, name):
        '''Try to find the container ID with the specified name'''
        container = self._containers.get(name, None)
        if not container is None:
            return container.get('id', None)
        return None