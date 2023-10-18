def mget(self, keys, *args):
        """
        Returns a list of values ordered identically to ``keys``
        """
        args = list_or_args(keys, args)
        server_keys = {}
        ret_dict = {}
        for key in args:
            server_name = self.get_server_name(key)
            server_keys[server_name] = server_keys.get(server_name, [])
            server_keys[server_name].append(key)
        for server_name, sub_keys in iteritems(server_keys):
            values = self.connections[server_name].mget(sub_keys)
            ret_dict.update(dict(zip(sub_keys, values)))
        result = []
        for key in args:
            result.append(ret_dict.get(key, None))
        return result