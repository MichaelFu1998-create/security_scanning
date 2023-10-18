def sendToSbs(self, challenge_id, item_id):
        """Send card FROM CLUB to first free slot in sbs squad."""
        # TODO?: multiple item_ids
        method = 'PUT'
        url = 'sbs/challenge/%s/squad' % challenge_id

        squad = self.sbsSquad(challenge_id)
        players = []
        moved = False
        n = 0
        for i in squad['squad']['players']:
            if i['itemData']['id'] == item_id:  # item already in sbs  # TODO?: report reason
                return False
            if i['itemData']['id'] == 0 and not moved:
                i['itemData']['id'] = item_id
                moved = True
            players.append({"index": n,
                            "itemData": {"id": i['itemData']['id'],
                                         "dream": False}})
            n += 1
        data = {'players': players}

        if not moved:
            return False
        else:
            self.__request__(method, url, data=json.dumps(data))
            return True