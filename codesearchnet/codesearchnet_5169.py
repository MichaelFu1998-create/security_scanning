def get_all_load_balancers(self):
        """
            Returns a list of Load Balancer objects.
        """
        data = self.get_data("load_balancers")

        load_balancers = list()
        for jsoned in data['load_balancers']:
            load_balancer = LoadBalancer(**jsoned)
            load_balancer.token = self.token
            load_balancer.health_check = HealthCheck(**jsoned['health_check'])
            load_balancer.sticky_sessions = StickySesions(**jsoned['sticky_sessions'])
            forwarding_rules = list()
            for rule in jsoned['forwarding_rules']:
                forwarding_rules.append(ForwardingRule(**rule))
            load_balancer.forwarding_rules = forwarding_rules
            load_balancers.append(load_balancer)
        return load_balancers