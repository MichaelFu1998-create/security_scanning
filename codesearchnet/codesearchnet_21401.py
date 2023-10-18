def object_to_id(self, obj):
        """
            Searches elasticsearch for objects with the same address, protocol, port and state.
        """
        search = Service.search()
        search = search.filter("term", address=obj.address)
        search = search.filter("term", protocol=obj.protocol)
        search = search.filter("term", port=obj.port)
        search = search.filter("term", state=obj.state)
        if search.count():
            result = search[0].execute()[0]
            return result.meta.id
        else:
            return None