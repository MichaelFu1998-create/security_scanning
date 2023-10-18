def add_forwarding_rules(self, forwarding_rules):
        """
        Adds new forwarding rules to a LoadBalancer.

        Args:
            forwarding_rules (obj:`list`): A list of `ForwrdingRules` objects
        """
        rules_dict = [rule.__dict__ for rule in forwarding_rules]

        return self.get_data(
            "load_balancers/%s/forwarding_rules/" % self.id,
            type=POST,
            params={"forwarding_rules": rules_dict}
        )