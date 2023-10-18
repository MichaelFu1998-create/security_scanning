async def rt_connect(self, loop):
        """Start subscription manager for real time data."""
        if self.sub_manager is not None:
            return
        self.sub_manager = SubscriptionManager(
            loop, "token={}".format(self._access_token), SUB_ENDPOINT
        )
        self.sub_manager.start()