def get_active_bets(self, project_id=None):
        '''Returns all active bets'''
        url = urljoin(
            self.settings['bets_url'],
            'bets?state=fresh,active,accept_end&page=1&page_size=100')

        if project_id is not None:
            url += '&kava_project_id={}'.format(project_id)

        bets = []
        has_next_page = True
        while has_next_page:
            res = self._req(url)
            bets.extend(res['bets']['results'])
            url = res['bets'].get('next')
            has_next_page = bool(url)

        return bets