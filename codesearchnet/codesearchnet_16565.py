async def rt_unsubscribe(self):
        """Unsubscribe to Tibber rt subscription."""
        if self._subscription_id is None:
            _LOGGER.error("Not subscribed.")
            return
        await self._tibber_control.sub_manager.unsubscribe(self._subscription_id)