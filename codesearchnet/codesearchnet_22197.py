def from_server(cls, server, slug, identifier):
        """Retrieve a task from the server"""
        task = server.get(
            'task',
            replacements={
                'slug': slug,
                'identifier': identifier})
        return cls(**task)