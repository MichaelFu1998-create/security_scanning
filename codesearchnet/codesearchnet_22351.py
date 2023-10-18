def get_fuel_prices(self) -> GetFuelPricesResponse:
        """Fetches fuel prices for all stations."""
        response = requests.get(
            '{}/prices'.format(API_URL_BASE),
            headers=self._get_headers(),
            timeout=self._timeout,
        )

        if not response.ok:
            raise FuelCheckError.create(response)

        return GetFuelPricesResponse.deserialize(response.json())