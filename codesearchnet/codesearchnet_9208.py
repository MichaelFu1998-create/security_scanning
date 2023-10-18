def __create_arthur_json(self, repo, backend_args):
        """ Create the JSON for configuring arthur to collect data

        https://github.com/grimoirelab/arthur#adding-tasks
        Sample for git:

        {
        "tasks": [
            {
                "task_id": "arthur.git",
                "backend": "git",
                "backend_args": {
                    "gitpath": "/tmp/arthur_git/",
                    "uri": "https://github.com/grimoirelab/arthur.git"
                },
                "category": "commit",
                "archive_args": {
                    "archive_path": '/tmp/test_archives',
                    "fetch_from_archive": false,
                    "archive_after": None
                },
                "scheduler_args": {
                    "delay": 10
                }
            }
        ]
        }
        """

        backend_args = self._compose_arthur_params(self.backend_section, repo)
        if self.backend_section == 'git':
            backend_args['gitpath'] = os.path.join(self.REPOSITORY_DIR, repo)
        backend_args['tag'] = self.backend_tag(repo)

        ajson = {"tasks": [{}]}
        # This is the perceval tag
        ajson["tasks"][0]['task_id'] = self.backend_tag(repo)
        ajson["tasks"][0]['backend'] = self.backend_section.split(":")[0]
        ajson["tasks"][0]['backend_args'] = backend_args
        ajson["tasks"][0]['category'] = backend_args['category']
        ajson["tasks"][0]['archive'] = {}
        ajson["tasks"][0]['scheduler'] = {"delay": self.ARTHUR_TASK_DELAY}
        # from-date or offset param must be added
        es_col_url = self._get_collection_url()
        es_index = self.conf[self.backend_section]['raw_index']
        # Get the last activity for the data source
        es = ElasticSearch(es_col_url, es_index)
        connector = get_connector_from_name(self.backend_section)

        klass = connector[0]  # Backend for the connector
        signature = inspect.signature(klass.fetch)

        last_activity = None
        filter_ = {"name": "tag", "value": backend_args['tag']}
        if 'from_date' in signature.parameters:
            last_activity = es.get_last_item_field('metadata__updated_on', [filter_])
            if last_activity:
                ajson["tasks"][0]['backend_args']['from_date'] = last_activity.isoformat()
        elif 'offset' in signature.parameters:
            last_activity = es.get_last_item_field('offset', [filter_])
            if last_activity:
                ajson["tasks"][0]['backend_args']['offset'] = last_activity

        if last_activity:
            logging.info("Getting raw item with arthur since %s", last_activity)

        return(ajson)