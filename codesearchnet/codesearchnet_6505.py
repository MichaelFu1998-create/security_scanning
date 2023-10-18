def browse(self, cat=None, subCat=None):
        """Browse categories. If neither cat nor subcat are specified,
        return a list of categories, otherwise it return a list of apps
        using cat (category ID) and subCat (subcategory ID) as filters."""
        path = BROWSE_URL + "?c=3"
        if cat is not None:
            path += "&cat={}".format(requests.utils.quote(cat))
        if subCat is not None:
            path += "&ctr={}".format(requests.utils.quote(subCat))
        data = self.executeRequestApi2(path)

        return utils.parseProtobufObj(data.payload.browseResponse)