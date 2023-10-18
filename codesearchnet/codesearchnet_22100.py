def update(self, server):
        """Update existing tasks on the server"""
        for chunk in self.__cut_to_size():
            server.put(
                'tasks_admin',
                chunk.as_payload(),
                replacements={
                    'slug': chunk.challenge.slug})