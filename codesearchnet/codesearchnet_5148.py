def add_tags(self, tags):
        """
            Add tags to this Firewall.
        """
        return self.get_data(
            "firewalls/%s/tags" % self.id,
            type=POST,
            params={"tags": tags}
        )