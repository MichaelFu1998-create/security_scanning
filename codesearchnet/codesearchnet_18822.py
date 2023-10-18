def _login(self, session, get_request=False):
        """Return a session for yesss.at."""
        req = session.post(self._login_url, data=self._logindata)
        if _LOGIN_ERROR_STRING in req.text or \
                req.status_code == 403 or \
                req.url == _LOGIN_URL:
            err_mess = "YesssSMS: login failed, username or password wrong"

            if _LOGIN_LOCKED_MESS in req.text:
                err_mess += ", page says: " + _LOGIN_LOCKED_MESS_ENG
                self._suspended = True
                raise self.AccountSuspendedError(err_mess)
            raise self.LoginError(err_mess)

        self._suspended = False  # login worked

        return (session, req) if get_request else session