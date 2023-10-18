def create_datacenter(self, datacenter):
        """
        Creates a data center -- both simple and complex are supported.

        """
        server_items = []
        volume_items = []
        lan_items = []
        loadbalancer_items = []

        entities = dict()

        properties = {
            "name": datacenter.name
        }

        # Omit 'location', if not provided, to receive
        # a meaningful error message.
        if datacenter.location:
            properties['location'] = datacenter.location

        # Optional Properties
        if datacenter.description:
            properties['description'] = datacenter.description

        # Servers
        if datacenter.servers:
            for server in datacenter.servers:
                server_items.append(self._create_server_dict(server))

            servers = {
                "items": server_items
            }

            server_entities = {
                "servers": servers
            }

            entities.update(server_entities)

        # Volumes
        if datacenter.volumes:
            for volume in datacenter.volumes:
                volume_items.append(self._create_volume_dict(volume))

            volumes = {
                "items": volume_items
            }

            volume_entities = {
                "volumes": volumes
            }

            entities.update(volume_entities)

        # Load Balancers
        if datacenter.loadbalancers:
            for loadbalancer in datacenter.loadbalancers:
                loadbalancer_items.append(
                    self._create_loadbalancer_dict(
                        loadbalancer
                    )
                )

            loadbalancers = {
                "items": loadbalancer_items
            }

            loadbalancer_entities = {
                "loadbalancers": loadbalancers
            }

            entities.update(loadbalancer_entities)

        # LANs
        if datacenter.lans:
            for lan in datacenter.lans:
                lan_items.append(
                    self._create_lan_dict(lan)
                )

            lans = {
                "items": lan_items
            }

            lan_entities = {
                "lans": lans
            }

            entities.update(lan_entities)

        if not entities:
            raw = {
                "properties": properties,
            }
        else:
            raw = {
                "properties": properties,
                "entities": entities
            }

        data = json.dumps(raw)

        response = self._perform_request(
            url='/datacenters',
            method='POST',
            data=data)

        return response