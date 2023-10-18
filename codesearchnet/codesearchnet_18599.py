def process_response(self, resp, multiple_rates):
        """ Get the tax rate from the ZipTax response """
        self._check_for_exceptions(resp, multiple_rates)

        rates = {}
        for result in resp['results']:
            rate = ZipTaxClient._cast_tax_rate(result['taxSales'])
            rates[result['geoCity']] = rate
        if not multiple_rates:
            return rates[list(rates.keys())[0]]
        return rates