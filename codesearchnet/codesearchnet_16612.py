def post_process(self, group, event, is_new, is_sample, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        host = self.get_option('server_host', group.project)
        port = int(self.get_option('server_port', group.project))
        prefix = self.get_option('prefix', group.project)
        hostname = self.get_option('hostname', group.project) or socket.gethostname()
        resolve_age = group.project.get_option('sentry:resolve_age', None)

        now = int(time.time())
        template = '%s.%%s[%s]' % (prefix, group.project.slug)

        level = group.get_level_display()
        label = template % level

        groups = group.project.group_set.filter(status=STATUS_UNRESOLVED)

        if resolve_age:
            oldest = timezone.now() - timedelta(hours=int(resolve_age))
            groups = groups.filter(last_seen__gt=oldest)

        num_errors = groups.filter(level=group.level).count()

        metric = Metric(hostname, label, num_errors, now)

        log.info('will send %s=%s to zabbix', label, num_errors)

        send_to_zabbix([metric], host, port)