def currency(self):
        """Return the currency."""
        try:
            current_subscription = self.info["viewer"]["home"]["currentSubscription"]
            return current_subscription["priceInfo"]["current"]["currency"]
        except (KeyError, TypeError, IndexError):
            _LOGGER.error("Could not find currency.")
        return ""