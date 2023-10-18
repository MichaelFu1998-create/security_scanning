def logout(self, save=True):
        """Log out nicely (like clicking on logout button).

        :params save: False if You don't want to save cookies.
        """
        # self.r.get('https://www.easports.com/signout', params={'ct': self._})
        # self.r.get('https://accounts.ea.com/connect/clearsid', params={'ct': self._})
        # self.r.get('https://beta.www.origin.com/views/logout.html', params={'ct': self._})
        # self.r.get('https://help.ea.com/community/logout/', params={'ct': self._})
        self.r.delete('https://%s/ut/auth' % self.fut_host, timeout=self.timeout)
        if save:
            self.saveSession()
        # needed? https://accounts.ea.com/connect/logout?client_id=FIFA-18-WEBCLIENT&redirect_uri=https://www.easports.com/fifa/ultimate-team/web-app/auth.html
        return True