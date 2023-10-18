def on_message(self, websocket, message):
        '''Handle websocket incoming messages
        '''
        waiter = self._waiter
        self._waiter = None
        encoded = json.loads(message)
        event = encoded.get('event')
        channel = encoded.get('channel')
        data = json.loads(encoded.get('data'))
        try:
            if event == PUSHER_ERROR:
                raise PusherError(data['message'], data['code'])
            elif event == PUSHER_CONNECTION:
                self.socket_id = data.get('socket_id')
                self.logger.info('Succesfully connected on socket %s',
                                 self.socket_id)
                waiter.set_result(self.socket_id)
            elif event == PUSHER_SUBSCRIBED:
                self.logger.info('Succesfully subscribed to %s',
                                 encoded.get('channel'))
            elif channel:
                self[channel]._event(event, data)
        except Exception as exc:
            if waiter:
                waiter.set_exception(exc)
            else:
                self.logger.exception('pusher error')