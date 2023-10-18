def save(self):
        """Saves this order to Holvi, returns a tuple with the order itself and checkout_uri"""
        if self.code:
            raise HolviError("Orders cannot be updated")
        send_json = self.to_holvi_dict()
        send_json.update({
            'pool': self.api.connection.pool
        })
        url = six.u(self.api.base_url + "order/")
        stat = self.api.connection.make_post(url, send_json)
        code = stat["details_uri"].split("/")[-2]  # Maybe slightly ugly but I don't want to basically reimplement all but uri formation of the api method
        return (stat["checkout_uri"], self.api.get_order(code))