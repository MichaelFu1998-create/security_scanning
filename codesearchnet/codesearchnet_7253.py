async def send_maps(self, map_list):
        """Sends a request to the server containing maps (dicts)."""
        params = {
            'VER': 8,  # channel protocol version
            'RID': 81188,  # request identifier
            'ctype': 'hangouts',  # client type
        }
        if self._gsessionid_param is not None:
            params['gsessionid'] = self._gsessionid_param
        if self._sid_param is not None:
            params['SID'] = self._sid_param
        data_dict = dict(count=len(map_list), ofs=0)
        for map_num, map_ in enumerate(map_list):
            for map_key, map_val in map_.items():
                data_dict['req{}_{}'.format(map_num, map_key)] = map_val
        res = await self._session.fetch(
            'post', CHANNEL_URL, params=params, data=data_dict
        )
        return res