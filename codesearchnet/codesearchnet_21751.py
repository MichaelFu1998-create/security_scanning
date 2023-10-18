def load(cls, query_name):
        """Load a pre-made query.

        These queries are distributed with lsstprojectmeta. See
        :file:`lsstrojectmeta/data/githubv4/README.rst` inside the
        package repository for details on available queries.

        Parameters
        ----------
        query_name : `str`
            Name of the query, such as ``'technote_repo'``.

        Returns
        -------
        github_query : `GitHubQuery
            A GitHub query or mutation object that you can pass to
            `github_request` to execute the request itself.
        """
        template_path = os.path.join(
            os.path.dirname(__file__),
            '../data/githubv4',
            query_name + '.graphql')

        with open(template_path) as f:
            query_data = f.read()

        return cls(query_data, name=query_name)