def club(self, sort='desc', ctype='player', defId='', start=0, count=None, page_size=itemsPerPage['club'],
             level=None, category=None, assetId=None, league=None, club=None,
             position=None, zone=None, nationality=None, rare=False, playStyle=None):
        """Return items in your club, excluding consumables.

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
        :param page_size: (optional) Page size (items per page)
        """
        method = 'GET'
        url = 'club'

        if count:  # backward compatibility, will be removed in future
            page_size = count

        params = {'sort': sort, 'type': ctype, 'defId': defId, 'start': start, 'count': page_size}
        if level:
            params['level'] = level
        if category:
            params['cat'] = category
        if assetId:
            params['maskedDefId'] = assetId
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
        rc = self.__request__(method, url, params=params)

        # pinEvent
        if start == 0:
            if ctype == 'player':
                pgid = 'Club - Players - List View'
            elif ctype == 'staff':
                pgid = 'Club - Staff - List View'
            elif ctype in ('item', 'kit', 'ball', 'badge', 'stadium'):
                pgid = 'Club - Club Items - List View'
            # else:  # TODO: THIS IS probably WRONG, detect all ctypes
            #     pgid = 'Club - Club Items - List View'
            events = [self.pin.event('page_view', 'Hub - Club'), self.pin.event('page_view', pgid)]
            if rc['itemData']:
                events.append(self.pin.event('page_view', 'Item - Detail View'))
            self.pin.send(events)

        return [itemParse({'itemData': i}) for i in rc['itemData']]