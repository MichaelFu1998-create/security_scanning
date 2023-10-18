def create(self, *args, **kwargs):
        """
        Creates a new LoadBalancer.

        Note: Every argument and parameter given to this method will be
        assigned to the object.

        Args:
            name (str): The Load Balancer's name
            region (str): The slug identifier for a DigitalOcean region
            algorithm (str, optional): The load balancing algorithm to be
                used. Currently, it must be either "round_robin" or
                "least_connections"
            forwarding_rules (obj:`list`): A list of `ForwrdingRules` objects
            health_check (obj, optional): A `HealthCheck` object
            sticky_sessions (obj, optional): A `StickySessions` object
            redirect_http_to_https (bool, optional): A boolean indicating
                whether HTTP requests to the Load Balancer should be
                redirected to HTTPS
            droplet_ids (obj:`list` of `int`): A list of IDs representing
                Droplets to be added to the Load Balancer (mutually
                exclusive with 'tag')
            tag (str): A string representing a DigitalOcean Droplet tag
                (mutually exclusive with 'droplet_ids')
        """
        rules_dict = [rule.__dict__ for rule in self.forwarding_rules]

        params = {'name': self.name, 'region': self.region,
                  'forwarding_rules': rules_dict,
                  'redirect_http_to_https': self.redirect_http_to_https}

        if self.droplet_ids and self.tag:
            raise ValueError('droplet_ids and tag are mutually exclusive args')
        elif self.tag:
            params['tag'] = self.tag
        else:
            params['droplet_ids'] = self.droplet_ids

        if self.algorithm:
            params['algorithm'] = self.algorithm
        if self.health_check:
            params['health_check'] = self.health_check.__dict__
        if self.sticky_sessions:
            params['sticky_sessions'] = self.sticky_sessions.__dict__

        data = self.get_data('load_balancers/', type=POST, params=params)

        if data:
            self.id = data['load_balancer']['id']
            self.ip = data['load_balancer']['ip']
            self.algorithm = data['load_balancer']['algorithm']
            self.health_check = HealthCheck(
                **data['load_balancer']['health_check'])
            self.sticky_sessions = StickySesions(
                **data['load_balancer']['sticky_sessions'])
            self.droplet_ids = data['load_balancer']['droplet_ids']
            self.status = data['load_balancer']['status']
            self.created_at = data['load_balancer']['created_at']

        return self