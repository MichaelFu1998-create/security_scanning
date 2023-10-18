def tsne(self, data_view_id):
        """
        Get the t-SNE projection, including responses and tags.

        :param data_view_id: The ID of the data view to retrieve TSNE from
        :type data_view_id: int
        :return: The TSNE analysis
        :rtype: :class:`Tsne`
        """
        analysis = self._data_analysis(data_view_id)
        projections = analysis['projections']
        tsne = Tsne()
        for k, v in projections.items():
            projection = Projection(
                xs=v['x'],
                ys=v['y'],
                responses=v['label'],
                tags=v['inputs'],
                uids=v['uid']
            )
            tsne.add_projection(k, projection)

        return tsne