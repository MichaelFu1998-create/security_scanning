def get_datacenter_by_name(self, name, depth=1):
        """
        Retrieves a data center by its name.

        Either returns the data center response or raises an Exception
        if no or more than one data center was found with the name.
        The search for the name is done in this relaxing way:

        - exact name match
        - case-insentive name match
        - data center starts with the name
        - data center starts with the name  (case insensitive)
        - name appears in the data center name
        - name appears in the data center name (case insensitive)

        :param      name: The name of the data center.
        :type       name: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``
        """
        all_data_centers = self.list_datacenters(depth=depth)['items']
        data_center = find_item_by_name(all_data_centers, lambda i: i['properties']['name'], name)
        if not data_center:
            raise NameError("No data center found with name "
                            "containing '{name}'.".format(name=name))
        if len(data_center) > 1:
            raise NameError("Found {n} data centers with the name '{name}': {names}".format(
                n=len(data_center),
                name=name,
                names=", ".join(d['properties']['name'] for d in data_center)
            ))
        return data_center[0]