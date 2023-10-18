def expose_ancestors_or_children(self, member, collection, lang=None):
        """ Build an ancestor or descendant dict view based on selected information

        :param member: Current Member to build for
        :param collection: Collection from which we retrieved it
        :param lang: Language to express data in
        :return:
        """
        x = {
            "id": member.id,
            "label": str(member.get_label(lang)),
            "model": str(member.model),
            "type": str(member.type),
            "size": member.size,
            "semantic": self.semantic(member, parent=collection)
        }
        if isinstance(member, ResourceCollection):
            x["lang"] = str(member.lang)
        return x