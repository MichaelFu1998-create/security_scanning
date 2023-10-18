def object_to_id(self, obj):
        """
            Searches elasticsearch for objects with the same username, password, optional domain, host_ip and service_id.
        """
        # Not sure yet if this is advisable... Older passwords can be overwritten...
        search = Credential.search()
        search = search.filter("term", username=obj.username)
        search = search.filter("term", secret=obj.secret)
        if obj.domain:
            search = search.filter("term", domain=obj.domain)
        else:
            search = search.exclude("exists", field="domain")
        if obj.host_ip:
            search = search.filter("term", host_ip=obj.host_ip)
        else:
            search = search.exclude("exists", field="host_ip")
        if obj.service_id:
            search = search.filter("term", service_id=obj.service_id)
        else:
            search = search.exclude("exists", field="service_id")
        if search.count():
            result = search[0].execute()[0]
            return result.meta.id
        else:
            return None