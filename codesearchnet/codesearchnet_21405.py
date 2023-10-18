def find_object(self, username, secret, domain=None, host_ip=None, service_id=None):
        """
            Searches elasticsearch for objects with the same username, password, optional domain, host_ip and service_id.
        """
        # Not sure yet if this is advisable... Older passwords can be overwritten...
        search = Credential.search()
        search = search.filter("term", username=username)
        search = search.filter("term", secret=secret)
        if domain:
            search = search.filter("term", domain=domain)
        else:
            search = search.exclude("exists", field="domain")
        if host_ip:
            search = search.filter("term", host_ip=host_ip)
        else:
            search = search.exclude("exists", field="host_ip")
        if service_id:
            search = search.filter("term", service_id=service_id)
        else:
            search = search.exclude("exists", field="service_id")
        if search.count():
            result = search[0].execute()[0]
            return result
        else:
            return None