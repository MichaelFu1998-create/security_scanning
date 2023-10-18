async def get_historic_data(self, n_data):
        """Get historic data."""
        query = gql(
            """
                {
                  viewer {
                    home(id: "%s") {
                      consumption(resolution: HOURLY, last: %s) {
                        nodes {
                          from
                          totalCost
                          consumption
                        }
                      }
                    }
                  }
                }
          """
            % (self.home_id, n_data)
        )
        data = await self._tibber_control.execute(query)
        if not data:
            _LOGGER.error("Could not find current the data.")
            return
        data = data["viewer"]["home"]["consumption"]
        if data is None:
            self._data = []
            return
        self._data = data["nodes"]