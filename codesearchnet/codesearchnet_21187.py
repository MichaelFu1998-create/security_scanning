def get(self, pk, cascadeFetch=False):
		'''
			get - Get a single value with the internal primary key.


			@param cascadeFetch <bool> Default False, If True, all Foreign objects associated with this model
			   will be fetched immediately. If False, foreign objects will be fetched on-access.

			@param pk - internal primary key (can be found via .getPk() on an item)
		'''
		conn = self._get_connection()
		key = self._get_key_for_id(pk)
		res = conn.hgetall(key)
		if type(res) != dict or not len(res.keys()):
			return None
		res['_id'] = pk

		ret = self._redisResultToObj(res)
		if cascadeFetch is True:
			self._doCascadeFetch(ret)
		return ret