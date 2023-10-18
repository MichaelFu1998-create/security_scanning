def make_parents(self, collection, lang=None):
        """ Build parents list for given collection

        :param collection: Collection to build dict view of for its members
        :param lang: Language to express data in
        :return: List of basic objects
        """
        return [
            {
                "id": member.id,
                "label": str(member.get_label(lang)),
                "model": str(member.model),
                "type": str(member.type),
                "size": member.size
            }
            for member in collection.parents
            if member.get_label()
        ]