async def set_tz(self):
        """
            set the environment timezone to the timezone
            set in your twitter settings
        """
        settings = await self.api.account.settings.get()

        tz = settings.time_zone.tzinfo_name

        os.environ['TZ'] = tz
        time.tzset()