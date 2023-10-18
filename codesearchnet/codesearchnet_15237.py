async def update(self) -> None:
        """Force update of alarm status and zones"""
        _LOGGER.debug("Requesting state update from server (S00, S14)")
        await asyncio.gather(
            # List unsealed Zones
            self.send_command('S00'),
            # Arming status update
            self.send_command('S14'),
        )