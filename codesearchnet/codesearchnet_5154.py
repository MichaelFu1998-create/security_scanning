def edit(self):
        """
            Edit the SSH Key
        """
        input_params = {
            "name": self.name,
            "public_key": self.public_key,
        }

        data = self.get_data(
            "account/keys/%s" % self.id,
            type=PUT,
            params=input_params
        )

        if data:
            self.id = data['ssh_key']['id']