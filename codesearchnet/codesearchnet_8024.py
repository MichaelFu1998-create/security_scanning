def destroy(self):
        """ Destroys the Lavalink client. """
        self.ws.destroy()
        self.bot.remove_listener(self.on_socket_response)
        self.hooks.clear()