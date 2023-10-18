def get_bets(self, type=None, order_by=None, state=None, project_id=None,
                 page=None, page_size=None):
        """Return bets with given filters and ordering.

        :param type: return bets only with this type.
                     Use None to include all (default).
        :param order_by: '-last_stake' or 'last_stake' to sort by stake's
                         created date or None for default ordering.
        :param state: one of 'active', 'closed', 'all' (default 'active').
        :param project_id: return bets associated with given project id in kava
        :param page: default 1.
        :param page_site: page size (default 100).
        """
        if page is None:
            page = 1
        if page_size is None:
            page_size = 100
        if state == 'all':
            _states = []  # all states == no filter
        elif state == 'closed':
            _states = self.CLOSED_STATES
        else:
            _states = self.ACTIVE_STATES

        url = urljoin(
            self.settings['bets_url'],
            'bets?page={}&page_size={}'.format(page, page_size))
        url += '&state={}'.format(','.join(_states))
        if type is not None:
            url += '&type={}'.format(type)
        if order_by in ['-last_stake', 'last_stake']:
            url += '&order_by={}'.format(order_by)
        if project_id is not None:
            url += '&kava_project_id={}'.format(project_id)

        res = self._req(url)
        return res['bets']['results']