def make_members(self, collection, lang=None):
        """ Build member list for given collection

        :param collection: Collection to build dict view of for its members
        :param lang: Language to express data in
        :return: List of basic objects
        """
        objects = sorted([
                self.expose_ancestors_or_children(member, collection, lang=lang)
                for member in collection.members
                if member.get_label()
            ],
            key=itemgetter("label")
        )
        return objects