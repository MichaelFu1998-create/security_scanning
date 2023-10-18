def get_address_coords(self, address):
        ''' Use the google geocoder to get latitude and longitude for an address string

        Args:
            address: any address string

        Returns:
            A tuple of (lat,lng)
        '''
        url = "https://maps.googleapis.com/maps/api/geocode/json?&address=" + address
        r = requests.get(url)
        r.raise_for_status()
        results = r.json()['results']
        lat = results[0]['geometry']['location']['lat']
        lng = results[0]['geometry']['location']['lng']
        return lat, lng