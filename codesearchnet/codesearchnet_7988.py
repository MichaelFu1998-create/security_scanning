def mset(self, mapping):
        """
        Sets each key in the ``mapping`` dict to its corresponding value
        """
        servers = {}
        for key, value in mapping.items():
            server_name = self.get_server_name(key)
            servers.setdefault(server_name, [])
            servers[server_name].append((key, value))
        for name, items in servers.items():
            self.connections[name].mset(dict(items))
        return True