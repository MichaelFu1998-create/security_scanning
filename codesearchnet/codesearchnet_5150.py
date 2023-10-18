def get_object(cls, api_token, ssh_key_id):
        """
            Class method that will return a SSHKey object by ID.
        """
        ssh_key = cls(token=api_token, id=ssh_key_id)
        ssh_key.load()
        return ssh_key