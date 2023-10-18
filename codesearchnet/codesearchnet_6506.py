def list(self, cat, ctr=None, nb_results=None, offset=None):
        """List all possible subcategories for a specific category. If
        also a subcategory is provided, list apps from this category.

        Args:
            cat (str): category id
            ctr (str): subcategory id
            nb_results (int): if a subcategory is specified, limit number
                of results to this number
            offset (int): if a subcategory is specified, start counting from this
                result
        Returns:
            A list of categories. If subcategory is specified, a list of apps in this
            category.
        """
        path = LIST_URL + "?c=3&cat={}".format(requests.utils.quote(cat))
        if ctr is not None:
            path += "&ctr={}".format(requests.utils.quote(ctr))
        if nb_results is not None:
            path += "&n={}".format(requests.utils.quote(str(nb_results)))
        if offset is not None:
            path += "&o={}".format(requests.utils.quote(str(offset)))
        data = self.executeRequestApi2(path)
        clusters = []
        docs = []
        if ctr is None:
            # list subcategories
            for pf in data.preFetch:
                for cluster in pf.response.payload.listResponse.doc:
                    clusters.extend(cluster.child)
            return [c.docid for c in clusters]
        else:
            apps = []
            for d in data.payload.listResponse.doc: # categories
                for c in d.child: # sub-category
                    for a in c.child: # app
                        apps.append(utils.parseProtobufObj(a))
            return apps