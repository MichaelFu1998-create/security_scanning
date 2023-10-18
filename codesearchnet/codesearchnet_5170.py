def get_load_balancer(self, id):
        """
            Returns a Load Balancer object by its ID.

            Args:
                id (str): Load Balancer ID
        """
        return LoadBalancer.get_object(api_token=self.token, id=id)