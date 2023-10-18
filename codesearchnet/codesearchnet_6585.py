def squad(self, squad_id=0, persona_id=None):
        """Return a squad.

        :params squad_id: Squad id.
        """
        method = 'GET'
        url = 'squad/%s/user/%s' % (squad_id, persona_id or self.persona_id)

        # pinEvents
        events = [self.pin.event('page_view', 'Hub - Squads')]
        self.pin.send(events)

        # TODO: ability to return other info than players only
        rc = self.__request__(method, url)

        # pinEvents
        events = [self.pin.event('page_view', 'Squad Details'), self.pin.event('page_view', 'Squads - Squad Overview')]
        self.pin.send(events)

        return [itemParse(i) for i in rc.get('players', ())]