async def websocket_send(self, message, stream_name):
        """
        Capture downstream websocket.send messages from the upstream applications.
        """
        text = message.get("text")
        # todo what to do on binary!
        json = await self.decode_json(text)
        data = {
            "stream": stream_name,
            "payload": json
        }
        await self.send_json(data)