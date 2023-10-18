def _fetch(self, method, url=None, post_data=None, parse_data=True, key=None, parameters=None, listener=None, full_return=False):
        """ Issue a request.

        Args:
            method (str): Request method (GET/POST/PUT/DELETE/etc.) If not specified, it will be POST if post_data is not None

        Kwargs:
            url (str): Destination URL
            post_data (str): A string of what to POST
            parse_data (bool): If true, parse response data
            key (string): If parse_data==True, look for this key when parsing data
            parameters (dict): Additional GET parameters to append to the URL
            listener (func): callback called when uploading a file
            full_return (bool): If set to True, get a full response (with success, data, info, body)

        Returns:
            dict. Response. If full_return==True, a dict with keys: success, data, info, body, otherwise the parsed data

        Raises:
            AuthenticationError, ConnectionError, urllib2.HTTPError, ValueError
        """

        headers = self.get_headers()
        headers["Content-Type"] = "application/json"

        handlers = []
        debuglevel = int(self._settings["debug"])
    
        handlers.append(urllib2.HTTPHandler(debuglevel=debuglevel))
        if hasattr(httplib, "HTTPS"):
            handlers.append(urllib2.HTTPSHandler(debuglevel=debuglevel))

        handlers.append(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

        password_url = self._get_password_url()
        if password_url and "Authorization" not in headers:
            pwd_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
            pwd_manager.add_password(None, password_url, self._settings["user"], self._settings["password"])
            handlers.append(HTTPBasicAuthHandler(pwd_manager))

        opener = urllib2.build_opener(*handlers)

        if post_data is not None:
            post_data = json.dumps(post_data)

        uri = self._url(url, parameters)
        request = RESTRequest(uri, method=method, headers=headers)
        if post_data is not None:
            request.add_data(post_data)

        response = None

        try:
            response = opener.open(request)
            body = response.read()
            if password_url and password_url not in self._settings["authorizations"] and request.has_header("Authorization"):
                self._settings["authorizations"][password_url] = request.get_header("Authorization")
        except urllib2.HTTPError as e:
            if e.code == 401:
                raise AuthenticationError("Access denied while trying to access %s" % uri)
            elif e.code == 404:
                raise ConnectionError("URL not found: %s" % uri)
            else:
                raise
        except urllib2.URLError as e:
            raise ConnectionError("Error while fetching from %s: %s" % (uri, e))
        finally:
            if response:
                response.close()

            opener.close()

        data = None
        if parse_data:
            if not key:
                key = string.split(url, "/")[0]

            data = self.parse(body, key)

        if full_return:
            info = response.info() if response else None
            status = int(string.split(info["status"])[0]) if (info and "status" in info) else None

            return {
                "success": (status >= 200 and status < 300), 
                "data": data, 
                "info": info, 
                "body": body
            }

        return data