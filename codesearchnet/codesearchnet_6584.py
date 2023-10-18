def clubConsumables(self, fast=False):
        """Return all consumables from club."""
        method = 'GET'
        url = 'club/consumables/development'

        rc = self.__request__(method, url)

        events = [self.pin.event('page_view', 'Hub - Club')]
        self.pin.send(events, fast=fast)
        events = [self.pin.event('page_view', 'Club - Consumables')]
        self.pin.send(events, fast=fast)
        events = [self.pin.event('page_view', 'Club - Consumables - List View')]
        self.pin.send(events, fast=fast)

        return [itemParse(i) for i in rc.get('itemData', ())]