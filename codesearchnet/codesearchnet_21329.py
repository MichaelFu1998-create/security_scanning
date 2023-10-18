def semantic(self, collection, parent=None):
        """ Generates a SEO friendly string for given collection

        :param collection: Collection object to generate string for
        :param parent: Current collection parent
        :return: SEO/URL Friendly string
        """
        if parent is not None:
            collections = parent.parents[::-1] + [parent, collection]
        else:
            collections = collection.parents[::-1] + [collection]

        return filters.slugify("--".join([item.get_label() for item in collections if item.get_label()]))