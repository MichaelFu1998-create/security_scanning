def tradepile(self):
        """Return items in tradepile."""
        method = 'GET'
        url = 'tradepile'

        rc = self.__request__(method, url)

        # pinEvents
        events = [self.pin.event('page_view', 'Hub - Transfers'), self.pin.event('page_view', 'Transfer List - List View')]
        if rc.get('auctionInfo'):
            events.append(self.pin.event('page_view', 'Item - Detail View'))
        self.pin.send(events)

        return [itemParse(i) for i in rc.get('auctionInfo', ())]