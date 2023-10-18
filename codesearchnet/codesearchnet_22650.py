def _url(self):
        """
        Resolve the URL to this point.

        >>> trello = TrelloAPIV1('APIKEY')
        >>> trello.batch._url
        '1/batch'
        >>> trello.boards(board_id='BOARD_ID')._url
        '1/boards/BOARD_ID'
        >>> trello.boards(board_id='BOARD_ID')(field='FIELD')._url
        '1/boards/BOARD_ID/FIELD'
        >>> trello.boards(board_id='BOARD_ID').cards(filter='FILTER')._url
        '1/boards/BOARD_ID/cards/FILTER'

        """
        if self._api_arg:
            mypart = str(self._api_arg)
        else:
            mypart = self._name

        if self._parent:
            return '/'.join(filter(None, [self._parent._url, mypart]))
        else:
            return mypart