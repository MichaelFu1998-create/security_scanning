def getOnlyFields(self, pk, fields, cascadeFetch=False):
		'''
			getOnlyFields - Gets only certain fields from a paticular primary key. For working on entire filter set, see allOnlyFields

			@param pk <int> - Primary Key

			@param fields list<str> - List of fields

			@param cascadeFetch <bool> Default False, If True, all Foreign objects associated with this model
			   will be fetched immediately. If False, foreign objects will be fetched on-access.


			return - Partial objects with only fields applied
		'''
		conn = self._get_connection()
		key = self._get_key_for_id(pk)

		res = conn.hmget(key, fields)
		if type(res) != list or not len(res):
			return None

		objDict = {}
		numFields = len(fields)
		i = 0
		anyNotNone = False
		while i < numFields:
			objDict[fields[i]] = res[i]
			if res[i] != None:
				anyNotNone = True
			i += 1

		if anyNotNone is False:
			return None
			
		objDict['_id'] = pk
		ret = self._redisResultToObj(objDict)
		if cascadeFetch is True:
			self._doCascadeFetch(ret)

		return ret