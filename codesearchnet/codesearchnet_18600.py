def _check_for_exceptions(self, resp, multiple_rates):
        """ Check if there are exceptions that should be raised """
        if resp['rCode'] != 100:
            raise exceptions.get_exception_for_code(resp['rCode'])(resp)

        results = resp['results']
        if len(results) == 0:
            raise exceptions.ZipTaxNoResults('No results found')
        if len(results) > 1 and not multiple_rates:
            # It's fine if all the taxes are the same
            rates = [result['taxSales'] for result in results]
            if len(set(rates)) != 1:
                raise exceptions.ZipTaxMultipleResults('Multiple results found but requested only one')