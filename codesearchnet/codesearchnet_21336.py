def r_references(self, objectId, lang=None):
        """ Text exemplar references browsing route function

        :param objectId: Collection identifier
        :type objectId: str
        :param lang: Lang in which to express main data
        :type lang: str
        :return: Template and required information about text with its references
        """
        collection, reffs = self.get_reffs(objectId=objectId, export_collection=True)
        return {
            "template": "main::references.html",
            "objectId": objectId,
            "citation": collection.citation,
            "collections": {
                "current": {
                    "label": collection.get_label(lang),
                    "id": collection.id,
                    "model": str(collection.model),
                    "type": str(collection.type),
                },
                "parents": self.make_parents(collection, lang=lang)
            },
            "reffs": reffs
        }