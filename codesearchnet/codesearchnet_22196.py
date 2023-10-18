def update(self, server):
        """Update existing task on the server"""
        return server.put(
            'task_admin',
            self.as_payload(),
            replacements={
                'slug': self.__challenge__.slug,
                'identifier': self.identifier})