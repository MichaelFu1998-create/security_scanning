def reports(self, **kwargs):
        """Get reports for our infrastructure. It is strongly recommended
        to include query and/or paging parameters for this endpoint to
        prevent large result sets and potential PuppetDB performance
        bottlenecks.

        :param \*\*kwargs: The rest of the keyword arguments are passed
                           to the _query function

        :returns: A generating yielding Reports
        :rtype: :class:`pypuppetdb.types.Report`
        """
        reports = self._query('reports', **kwargs)
        for report in reports:
            yield Report(
                api=self,
                node=report['certname'],
                hash_=report['hash'],
                start=report['start_time'],
                end=report['end_time'],
                received=report['receive_time'],
                version=report['configuration_version'],
                format_=report['report_format'],
                agent_version=report['puppet_version'],
                transaction=report['transaction_uuid'],
                environment=report['environment'],
                status=report['status'],
                noop=report.get('noop'),
                noop_pending=report.get('noop_pending'),
                metrics=report['metrics']['data'],
                logs=report['logs']['data'],
                code_id=report.get('code_id'),
                catalog_uuid=report.get('catalog_uuid'),
                cached_catalog_status=report.get('cached_catalog_status')
            )