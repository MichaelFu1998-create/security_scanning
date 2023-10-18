def main_collections(self, lang=None):
        """ Retrieve main parent collections of a repository

        :param lang: Language to retrieve information in
        :return: Sorted collections representations
        """
        return sorted([
            {
                "id": member.id,
                "label": str(member.get_label(lang=lang)),
                "model": str(member.model),
                "type": str(member.type),
                "size": member.size
            }
            for member in self.resolver.getMetadata().members
        ], key=itemgetter("label"))