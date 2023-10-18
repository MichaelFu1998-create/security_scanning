def get_clan_image(self, obj: BaseAttrDict):
        """Get the clan badge image URL

        Parameters
        ---------
        obj: official_api.models.BaseAttrDict
            An object that has the clan badge ID either in ``.clan.badge_id`` or ``.badge_id``
            Can be a clan or a profile for example.

        Returns str
        """

        try:
            badge_id = obj.clan.badge_id
        except AttributeError:
            try:
                badge_id = obj.badge_id
            except AttributeError:
                return 'https://i.imgur.com/Y3uXsgj.png'

        if badge_id is None:
            return 'https://i.imgur.com/Y3uXsgj.png'

        for i in self.constants.alliance_badges:
            if i.id == badge_id:
                return 'https://royaleapi.github.io/cr-api-assets/badges/' + i.name + '.png'