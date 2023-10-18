def get_arena_image(self, obj: BaseAttrDict):
        """Get the arena image URL

        Parameters
        ---------
        obj: official_api.models.BaseAttrDict
            An object that has the arena ID in ``.arena.id``
            Can be ``Profile`` for example.

        Returns None or str
        """
        badge_id = obj.arena.id
        for i in self.constants.arenas:
            if i.id == badge_id:
                return 'https://royaleapi.github.io/cr-api-assets/arenas/arena{}.png'.format(i.arena_id)