def create(self, server):
        """Create the tasks on the server"""
        for chunk in self.__cut_to_size():
            server.post(
                'tasks_admin',
                chunk.as_payload(),
                replacements={
                    'slug': chunk.challenge.slug})