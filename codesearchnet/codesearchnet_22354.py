def get_fuel_price_trends(self, latitude: float, longitude: float,
                              fuel_types: List[str]) -> PriceTrends:
        """Gets the fuel price trends for the given location and fuel types."""
        response = requests.post(
            '{}/prices/trends/'.format(API_URL_BASE),
            json={
                'location': {
                    'latitude': latitude,
                    'longitude': longitude,
                },
                'fueltypes': [{'code': type} for type in fuel_types],
            },
            headers=self._get_headers(),
            timeout=self._timeout,
        )

        if not response.ok:
            raise FuelCheckError.create(response)

        data = response.json()
        return PriceTrends(
            variances=[
                Variance.deserialize(variance)
                for variance in data['Variances']
            ],
            average_prices=[
                AveragePrice.deserialize(avg_price)
                for avg_price in data['AveragePrices']
            ]
        )