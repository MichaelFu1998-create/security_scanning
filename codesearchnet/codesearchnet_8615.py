def get_course_final_price(self, mode, currency='$', enterprise_catalog_uuid=None):
        """
        Get course mode's SKU discounted price after applying any entitlement available for this user.

        Returns:
            str: Discounted price of the course mode.

        """
        try:
            price_details = self.client.baskets.calculate.get(
                sku=[mode['sku']],
                username=self.user.username,
                catalog=enterprise_catalog_uuid,
            )
        except (SlumberBaseException, ConnectionError, Timeout) as exc:
            LOGGER.exception('Failed to get price details for sku %s due to: %s', mode['sku'], str(exc))
            price_details = {}
        price = price_details.get('total_incl_tax', mode['min_price'])
        if price != mode['min_price']:
            return format_price(price, currency)
        return mode['original_price']