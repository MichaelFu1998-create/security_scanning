def getMultipleOnlyFields(self, pks, fields, cascadeFetch=False):
		'''
			getMultipleOnlyFields - Gets only certain fields from a list of  primary keys. For working on entire filter set, see allOnlyFields

			@param pks list<str> - Primary Keys

			@param fields list<str> - List of fields


			@param cascadeFetch <bool> Default False, If True, all Foreign objects associated with this model
			   will be fetched immediately. If False, foreign objects will be fetched on-access.

			return - List of partial objects with only fields applied
		'''
		if type(pks) == set:
			pks = list(pks)

		if len(pks) == 1:
			return IRQueryableList([self.getOnlyFields(pks[0], fields, cascadeFetch=cascadeFetch)], mdl=self.mdl)

		conn = self._get_connection()
		pipeline = conn.pipeline()

		for pk in pks:
			key = self._get_key_for_id(pk)
			pipeline.hmget(key, fields)

		res = pipeline.execute()
		ret = IRQueryableList(mdl=self.mdl)
		pksLen = len(pks)
		i = 0
		numFields = len(fields)
		while i < pksLen:
			objDict = {}
			anyNotNone = False
			thisRes = res[i]
			if thisRes is None or type(thisRes) != list:
				ret.append(None)
				i += 1
				continue

			j = 0
			while j < numFields:
				objDict[fields[j]] = thisRes[j]
				if thisRes[j] != None:
					anyNotNone = True
				j += 1

			if anyNotNone is False:
				ret.append(None)
				i += 1
				continue

			objDict['_id'] = pks[i]
			obj = self._redisResultToObj(objDict)
			ret.append(obj)
			i += 1

		if cascadeFetch is True:
			for obj in ret:
				self._doCascadeFetch(obj)
			
		return ret