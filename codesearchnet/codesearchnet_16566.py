def rt_subscription_running(self):
        """Is real time subscription running."""
        return (
            self._tibber_control.sub_manager is not None
            and self._tibber_control.sub_manager.is_running
            and self._subscription_id is not None
        )