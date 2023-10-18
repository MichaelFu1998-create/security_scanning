def notify_listeners(self, data: Optional[_ListenableDataType]=_NO_DATA_MARKER):
        """
        Notify event listeners, passing them the given data (if any).
        :param data: the data to pass to the event listeners
        """
        for listener in self._listeners:
            if data is not Listenable._NO_DATA_MARKER:
                listener(data)
            else:
                listener()