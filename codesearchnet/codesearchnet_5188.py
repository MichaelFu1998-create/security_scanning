def remove_forwarding_rules(self, forwarding_rules):
        """
        Removes existing forwarding rules from a LoadBalancer.

        Args:
            forwarding_rules (obj:`list`): A list of `ForwrdingRules` objects
        """
        rules_dict = [rule.__dict__ for rule in forwarding_rules]

        return self.get_data(
            "load_balancers/%s/forwarding_rules/" % self.id,
            type=DELETE,
            params={"forwarding_rules": rules_dict}
        )