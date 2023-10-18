async def _get_response(self, message):
        """
        Get response running the view with await syntax if it is a
        coroutine function, otherwise just run it the normal way.
        """

        view = self.discovery_view(message)
        if not view:
            return

        if inspect.iscoroutinefunction(view):
            response = await view(message)
        else:
            response = view(message)

        return self.prepare_response(response, message)