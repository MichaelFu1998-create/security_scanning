async def send_notification(self, title, message):
        """Send notification."""
        query = gql(
            """
        mutation{
          sendPushNotification(input: {
            title: "%s",
            message: "%s",
          }){
            successful
            pushedToNumberOfDevices
          }
        }
        """
            % (title, message)
        )

        res = await self.execute(query)
        if not res:
            return False
        noti = res.get("sendPushNotification", {})
        successful = noti.get("successful", False)
        pushed_to_number_of_devices = noti.get("pushedToNumberOfDevices", 0)
        _LOGGER.debug(
            "send_notification: status %s, send to %s devices",
            successful,
            pushed_to_number_of_devices,
        )
        return successful