async def receive_json(self, content, **kwargs):
        """
        Rout the message down the correct stream.
        """
        # Check the frame looks good
        if isinstance(content, dict) and "stream" in content and "payload" in content:
            # Match it to a channel
            steam_name = content["stream"]
            payload = content["payload"]
            # block upstream frames
            if steam_name not in self.applications_accepting_frames:
                raise ValueError("Invalid multiplexed frame received (stream not mapped)")
            # send it on to the application that handles this stream
            await self.send_upstream(
                message={
                    "type": "websocket.receive",
                    "text": await self.encode_json(payload)
                },
                stream_name=steam_name
            )
            return
        else:
            raise ValueError("Invalid multiplexed **frame received (no channel/payload key)")