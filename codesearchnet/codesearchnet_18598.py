def make_request_data(self, zipcode, city, state):
        """ Make the request params given location data """
        data = {'key': self.api_key,
                'postalcode': str(zipcode),
                'city': city,
                'state': state
        }
        data = ZipTaxClient._clean_request_data(data)
        return data