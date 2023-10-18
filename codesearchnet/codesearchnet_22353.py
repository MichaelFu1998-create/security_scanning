def get_fuel_prices_within_radius(
            self, latitude: float, longitude: float, radius: int,
            fuel_type: str, brands: Optional[List[str]] = None
    ) -> List[StationPrice]:
        """Gets all the fuel prices within the specified radius."""

        if brands is None:
            brands = []
        response = requests.post(
            '{}/prices/nearby'.format(API_URL_BASE),
            json={
                'fueltype': fuel_type,
                'latitude': latitude,
                'longitude': longitude,
                'radius': radius,
                'brand': brands,
            },
            headers=self._get_headers(),
            timeout=self._timeout,
        )

        if not response.ok:
            raise FuelCheckError.create(response)

        data = response.json()
        stations = {
            station['code']: Station.deserialize(station)
            for station in data['stations']
        }
        station_prices = []  # type: List[StationPrice]
        for serialized_price in data['prices']:
            price = Price.deserialize(serialized_price)
            station_prices.append(StationPrice(
                price=price,
                station=stations[price.station_code]
            ))

        return station_prices