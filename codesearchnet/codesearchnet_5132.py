def create(self, *args, **kwargs):
        """
            Create the droplet with object properties.

            Note: Every argument and parameter given to this method will be
            assigned to the object.
        """
        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])

        # Provide backwards compatibility
        if not self.size_slug and self.size:
            self.size_slug = self.size

        ssh_keys_id = Droplet.__get_ssh_keys_id_or_fingerprint(self.ssh_keys,
                                                               self.token,
                                                               self.name)

        data = {
            "name": self.name,
            "size": self.size_slug,
            "image": self.image,
            "region": self.region,
            "ssh_keys": ssh_keys_id,
            "backups": bool(self.backups),
            "ipv6": bool(self.ipv6),
            "private_networking": bool(self.private_networking),
            "volumes": self.volumes,
            "tags": self.tags,
            "monitoring": bool(self.monitoring),
        }

        if self.user_data:
            data["user_data"] = self.user_data

        data = self.get_data("droplets/", type=POST, params=data)

        if data:
            self.id = data['droplet']['id']
            action_id = data['links']['actions'][0]['id']
            self.action_ids = []
            self.action_ids.append(action_id)