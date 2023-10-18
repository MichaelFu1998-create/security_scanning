def nodes(self, unreported=2, with_status=False, **kwargs):
        """Query for nodes by either name or query. If both aren't
        provided this will return a list of all nodes. This method
        also fetches the nodes status and event counts of the latest
        report from puppetdb.

        :param with_status: (optional) include the node status in the\
                           returned nodes
        :type with_status: :bool:
        :param unreported: (optional) amount of hours when a node gets
                           marked as unreported
        :type unreported: :obj:`None` or integer
        :param \*\*kwargs: The rest of the keyword arguments are passed
                           to the _query function

        :returns: A generator yieling Nodes.
        :rtype: :class:`pypuppetdb.types.Node`
        """
        nodes = self._query('nodes', **kwargs)
        now = datetime.datetime.utcnow()
        # If we happen to only get one node back it
        # won't be inside a list so iterating over it
        # goes boom. Therefor we wrap a list around it.
        if type(nodes) == dict:
            nodes = [nodes, ]

        if with_status:
            latest_events = self.event_counts(
                query=EqualsOperator("latest_report?", True),
                summarize_by='certname'
            )

        for node in nodes:
            node['status_report'] = None
            node['events'] = None

            if with_status:
                status = [s for s in latest_events
                          if s['subject']['title'] == node['certname']]

                try:
                    node['status_report'] = node['latest_report_status']

                    if status:
                        node['events'] = status[0]
                except KeyError:
                    if status:
                        node['events'] = status = status[0]
                        if status['successes'] > 0:
                            node['status_report'] = 'changed'
                        if status['noops'] > 0:
                            node['status_report'] = 'noop'
                        if status['failures'] > 0:
                            node['status_report'] = 'failed'
                    else:
                        node['status_report'] = 'unchanged'

                # node report age
                if node['report_timestamp'] is not None:
                    try:
                        last_report = json_to_datetime(
                            node['report_timestamp'])
                        last_report = last_report.replace(tzinfo=None)
                        unreported_border = now - timedelta(hours=unreported)
                        if last_report < unreported_border:
                            delta = (now - last_report)
                            node['unreported'] = True
                            node['unreported_time'] = '{0}d {1}h {2}m'.format(
                                delta.days,
                                int(delta.seconds / 3600),
                                int((delta.seconds % 3600) / 60)
                            )
                    except AttributeError:
                        node['unreported'] = True

                if not node['report_timestamp']:
                    node['unreported'] = True

            yield Node(self,
                       name=node['certname'],
                       deactivated=node['deactivated'],
                       expired=node['expired'],
                       report_timestamp=node['report_timestamp'],
                       catalog_timestamp=node['catalog_timestamp'],
                       facts_timestamp=node['facts_timestamp'],
                       status_report=node['status_report'],
                       noop=node.get('latest_report_noop'),
                       noop_pending=node.get('latest_report_noop_pending'),
                       events=node['events'],
                       unreported=node.get('unreported'),
                       unreported_time=node.get('unreported_time'),
                       report_environment=node['report_environment'],
                       catalog_environment=node['catalog_environment'],
                       facts_environment=node['facts_environment'],
                       latest_report_hash=node.get('latest_report_hash'),
                       cached_catalog_status=node.get('cached_catalog_status')
                       )