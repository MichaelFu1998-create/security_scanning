def search(self, ctype, level=None, category=None, assetId=None, defId=None,
               min_price=None, max_price=None, min_buy=None, max_buy=None,
               league=None, club=None, position=None, zone=None, nationality=None,
               rare=False, playStyle=None, start=0, page_size=itemsPerPage['transferMarket'],
               fast=False):
        """Prepare search request, send and return parsed data as a dict.

        :param ctype: [development / ? / ?] Card type.
        :param level: (optional) [?/?/gold] Card level.
        :param category: (optional) [fitness/?/?] Card category.
        :param assetId: (optional) Asset id.
        :param defId: (optional) Definition id.
        :param min_price: (optional) Minimal price.
        :param max_price: (optional) Maximum price.
        :param min_buy: (optional) Minimal buy now price.
        :param max_buy: (optional) Maximum buy now price.
        :param league: (optional) League id.
        :param club: (optional) Club id.
        :param position: (optional) Position.
        :param nationality: (optional) Nation id.
        :param rare: (optional) [boolean] True for searching special cards.
        :param playStyle: (optional) Play style.
        :param start: (optional) Start page sent to server so it supposed to be 12/15, 24/30 etc. (default platform page_size*n)
        :param page_size: (optional) Page size (items per page).
        """
        # TODO: add "search" alias
        # TODO: generator
        method = 'GET'
        url = 'transfermarket'

        # pinEvents
        if start == 0:
            events = [self.pin.event('page_view', 'Hub - Transfers'), self.pin.event('page_view', 'Transfer Market Search')]
            self.pin.send(events, fast=fast)

        params = {
            'start': start,
            'num': page_size,
            'type': ctype,  # "type" namespace is reserved in python
        }
        if level:
            params['lev'] = level
        if category:
            params['cat'] = category
        if assetId:
            params['maskedDefId'] = assetId
        if defId:
            params['definitionId'] = defId
        if min_price:
            params['micr'] = min_price
        if max_price:
            params['macr'] = max_price
        if min_buy:
            params['minb'] = min_buy
        if max_buy:
            params['maxb'] = max_buy
        if league:
            params['leag'] = league
        if club:
            params['team'] = club
        if position:
            params['pos'] = position
        if zone:
            params['zone'] = zone
        if nationality:
            params['nat'] = nationality
        if rare:
            params['rare'] = 'SP'
        if playStyle:
            params['playStyle'] = playStyle

        rc = self.__request__(method, url, params=params, fast=fast)

        # pinEvents
        if start == 0:
            events = [self.pin.event('page_view', 'Transfer Market Results - List View'), self.pin.event('page_view', 'Item - Detail View')]
            self.pin.send(events, fast=fast)

        return [itemParse(i) for i in rc.get('auctionInfo', ())]