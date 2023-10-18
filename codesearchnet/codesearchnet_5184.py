def save(self):
        """
        Save the LoadBalancer
        """
        forwarding_rules = [rule.__dict__ for rule in self.forwarding_rules]

        data = {
            'name': self.name,
            'region': self.region['slug'],
            'forwarding_rules': forwarding_rules,
            'redirect_http_to_https': self.redirect_http_to_https
        }

        if self.tag:
            data['tag'] = self.tag
        else:
            data['droplet_ids'] = self.droplet_ids

        if self.algorithm:
            data["algorithm"] = self.algorithm
        if self.health_check:
            data['health_check'] = self.health_check.__dict__
        if self.sticky_sessions:
            data['sticky_sessions'] = self.sticky_sessions.__dict__

        return self.get_data("load_balancers/%s/" % self.id,
                             type=PUT,
                             params=data)