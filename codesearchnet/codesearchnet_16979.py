def init_app(self, app,
                 entry_point_group_events='invenio_stats.events',
                 entry_point_group_aggs='invenio_stats.aggregations',
                 entry_point_group_queries='invenio_stats.queries'):
        """Flask application initialization."""
        self.init_config(app)

        state = _InvenioStatsState(
            app,
            entry_point_group_events=entry_point_group_events,
            entry_point_group_aggs=entry_point_group_aggs,
            entry_point_group_queries=entry_point_group_queries
        )
        self._state = app.extensions['invenio-stats'] = state

        if app.config['STATS_REGISTER_RECEIVERS']:
            signal_receivers = {key: value for key, value in
                                app.config.get('STATS_EVENTS', {}).items()
                                if 'signal' in value}
            register_receivers(app, signal_receivers)

        return state