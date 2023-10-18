def load(self):
        """
        Loads updated attributues for a LoadBalancer object.

        Requires self.id to be set.
        """
        data = self.get_data('load_balancers/%s' % self.id, type=GET)
        load_balancer = data['load_balancer']

        # Setting the attribute values
        for attr in load_balancer.keys():
            if attr == 'health_check':
                health_check = HealthCheck(**load_balancer['health_check'])
                setattr(self, attr, health_check)
            elif attr == 'sticky_sessions':
                sticky_ses = StickySesions(**load_balancer['sticky_sessions'])
                setattr(self, attr, sticky_ses)
            elif attr == 'forwarding_rules':
                rules = list()
                for rule in load_balancer['forwarding_rules']:
                    rules.append(ForwardingRule(**rule))
                setattr(self, attr, rules)
            else:
                setattr(self, attr, load_balancer[attr])

        return self