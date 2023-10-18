def create(self, server):
        """Create the task on the server"""
        if len(self.geometries) == 0:
            raise Exception('no geometries')
        return server.post(
            'task_admin',
            self.as_payload(),
            replacements={
                'slug': self.__challenge__.slug,
                'identifier': self.identifier})