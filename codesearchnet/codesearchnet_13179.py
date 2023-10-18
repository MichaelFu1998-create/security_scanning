def get_deck_link(self, deck: BaseAttrDict):
        """Form a deck link

        Parameters
        ---------
        deck: official_api.models.BaseAttrDict
            An object is a deck. Can be retrieved from ``Player.current_deck``

        Returns str
        """
        deck_link = 'https://link.clashroyale.com/deck/en?deck='

        for i in deck:
            card = self.get_card_info(i.name)
            deck_link += '{0.id};'.format(card)

        return deck_link