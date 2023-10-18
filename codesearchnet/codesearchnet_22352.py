def get_fuel_prices_for_station(
            self,
            station: int
    ) -> List[Price]:
        """Gets the fuel prices for a specific fuel station."""
        response = requests.get(
            '{}/prices/station/{}'.format(API_URL_BASE, station),
            headers=self._get_headers(),
            timeout=self._timeout,
        )

        if not response.ok:
            raise FuelCheckError.create(response)

        data = response.json()
        return [Price.deserialize(data) for data in data['prices']]