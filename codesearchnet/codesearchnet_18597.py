def get_rate(self, zipcode, city=None, state=None, multiple_rates=False):
        """
        Finds sales tax for given info.
        Returns Decimal of the tax rate, e.g. 8.750.
        """
        data = self.make_request_data(zipcode, city, state)

        r = requests.get(self.url, params=data)
        resp = r.json()

        return self.process_response(resp, multiple_rates)