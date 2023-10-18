def get_object(cls, api_token, id):
        """
        Class method that will return a LoadBalancer object by its ID.

        Args:
            api_token (str): DigitalOcean API token
            id (str): Load Balancer ID
        """
        load_balancer = cls(token=api_token, id=id)
        load_balancer.load()
        return load_balancer