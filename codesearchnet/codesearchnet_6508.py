def delivery(self, packageName, versionCode=None, offerType=1,
                 downloadToken=None, expansion_files=False):
        """Download an already purchased app.

        Args:
            packageName (str): app unique ID (usually starting with 'com.')
            versionCode (int): version to download
            offerType (int): different type of downloads (mostly unused for apks)
            downloadToken (str): download token returned by 'purchase' API
            progress_bar (bool): wether or not to print a progress bar to stdout

        Returns:
            Dictionary containing apk data and a list of expansion files. As stated
            in android documentation, there can be at most 2 expansion files, one with
            main content, and one for patching the main content. Their names should
            follow this format:

            [main|patch].<expansion-version>.<package-name>.obb

            Data to build this name string is provided in the dict object. For more
            info check https://developer.android.com/google/play/expansion-files.html
        """

        if versionCode is None:
            # pick up latest version
            versionCode = self.details(packageName).get('versionCode')

        params = {'ot': str(offerType),
                  'doc': packageName,
                  'vc': str(versionCode)}
        headers = self.getHeaders()
        if downloadToken is not None:
            params['dtok'] = downloadToken
        response = requests.get(DELIVERY_URL, headers=headers,
                                params=params, verify=ssl_verify,
                                timeout=60,
                                proxies=self.proxies_config)
        response = googleplay_pb2.ResponseWrapper.FromString(response.content)
        if response.commands.displayErrorMessage != "":
            raise RequestError(response.commands.displayErrorMessage)
        elif response.payload.deliveryResponse.appDeliveryData.downloadUrl == "":
            raise RequestError('App not purchased')
        else:
            result = {}
            result['docId'] = packageName
            result['additionalData'] = []
            downloadUrl = response.payload.deliveryResponse.appDeliveryData.downloadUrl
            cookie = response.payload.deliveryResponse.appDeliveryData.downloadAuthCookie[0]
            cookies = {
                str(cookie.name): str(cookie.value)
            }
            result['file'] = self._deliver_data(downloadUrl, cookies)
            if not expansion_files:
                return result
            for obb in response.payload.deliveryResponse.appDeliveryData.additionalFile:
                a = {}
                # fileType == 0 -> main
                # fileType == 1 -> patch
                if obb.fileType == 0:
                    obbType = 'main'
                else:
                    obbType = 'patch'
                a['type'] = obbType
                a['versionCode'] = obb.versionCode
                a['file'] = self._deliver_data(obb.downloadUrl, None)
                result['additionalData'].append(a)
            return result