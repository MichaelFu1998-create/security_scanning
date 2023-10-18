def price_unit(self):
        """Return the price unit."""
        currency = self.currency
        consumption_unit = self.consumption_unit
        if not currency or not consumption_unit:
            _LOGGER.error("Could not find price_unit.")
            return " "
        return currency + "/" + consumption_unit