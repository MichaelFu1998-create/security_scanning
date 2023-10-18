def remove_tags(self, tags):
        """
            Remove tags from this Firewall.
        """
        return self.get_data(
            "firewalls/%s/tags" % self.id,
            type=DELETE,
            params={"tags": tags}
        )