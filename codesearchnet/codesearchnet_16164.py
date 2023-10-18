async def message_handler(self, data):
        """
        For each new message, build its platform specific message
        object and get a response.
        """

        message = self.build_message(data)
        if not message:
            logger.error(
                '[%s] Unable to build Message with data, data=%s, error',
                self.engine_name,
                data
            )
            return

        logger.info('[%s] New message from %s: %s', self.engine_name,
                    message.user, message.text)

        response = await self.get_response(message)
        if response:
            await self.send_response(response)