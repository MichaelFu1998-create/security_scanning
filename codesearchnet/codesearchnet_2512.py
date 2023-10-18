def get(self):
    '''
    :return:
    '''
    clusters = yield access.get_clusters()

    # pylint: disable=no-member
    options = dict(
        topologies=[],  # no topologies
        clusters=[str(cluster) for cluster in clusters],
        active="topologies",  # active icon the nav bar
        function=common.className,
        baseUrl=self.baseUrl
    )

    # send the all topologies page
    self.render("topologies.html", **options)