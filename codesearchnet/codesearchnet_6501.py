def login(self, email=None, password=None, gsfId=None, authSubToken=None):
        """Login to your Google Account.
        For first time login you should provide:
            * email
            * password
        For the following logins you need to provide:
            * gsfId
            * authSubToken"""
        if email is not None and password is not None:
            # First time setup, where we obtain an ac2dm token and
            # upload device information

            encryptedPass = self.encryptPassword(email, password).decode('utf-8')
            # AC2DM token
            params = self.deviceBuilder.getLoginParams(email, encryptedPass)
            params['service'] = 'ac2dm'
            params['add_account'] = '1'
            params['callerPkg'] = 'com.google.android.gms'
            headers = self.deviceBuilder.getAuthHeaders(self.gsfId)
            headers['app'] = 'com.google.android.gsm'
            response = requests.post(AUTH_URL, data=params, verify=ssl_verify,
                                     proxies=self.proxies_config)
            data = response.text.split()
            params = {}
            for d in data:
                if "=" not in d:
                    continue
                k, v = d.split("=", 1)
                params[k.strip().lower()] = v.strip()
            if "auth" in params:
                ac2dmToken = params["auth"]
            elif "error" in params:
                if "NeedsBrowser" in params["error"]:
                    raise SecurityCheckError("Security check is needed, try to visit "
                                     "https://accounts.google.com/b/0/DisplayUnlockCaptcha "
                                     "to unlock, or setup an app-specific password")
                raise LoginError("server says: " + params["error"])
            else:
                raise LoginError("Auth token not found.")

            self.gsfId = self.checkin(email, ac2dmToken)
            self.getAuthSubToken(email, encryptedPass)
            self.uploadDeviceConfig()
        elif gsfId is not None and authSubToken is not None:
            # no need to initialize API
            self.gsfId = gsfId
            self.setAuthSubToken(authSubToken)
            # check if token is valid with a simple search
            self.search('drv')
        else:
            raise LoginError('Either (email,pass) or (gsfId, authSubToken) is needed')