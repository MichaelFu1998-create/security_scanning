def getMultiple(self, pks, cascadeFetch=False):
		'''
			getMultiple - Gets multiple objects with a single atomic operation


			@param cascadeFetch <bool> Default False, If True, all Foreign objects associated with this model
			   will be fetched immediately. If False, foreign objects will be fetched on-access.

			@param pks - list of internal keys
		'''

		if type(pks) == set:
			pks = list(pks)

		if len(pks) == 1:
			# Optimization to not pipeline on 1 id
			return IRQueryableList([self.get(pks[0], cascadeFetch=cascadeFetch)], mdl=self.mdl)

		conn = self._get_connection()
		pipeline = conn.pipeline()
		for pk in pks:
			key = self._get_key_for_id(pk)
			pipeline.hgetall(key)

		res = pipeline.execute()
		
		ret = IRQueryableList(mdl=self.mdl)
		i = 0
		pksLen = len(pks)
		while i < pksLen:
			if res[i] is None:
				ret.append(None)
				i += 1
				continue
			res[i]['_id'] = pks[i]
			obj = self._redisResultToObj(res[i])
			ret.append(obj)
			i += 1

		if cascadeFetch is True:
			for obj in ret:
				if not obj:
					continue
				self._doCascadeFetch(obj)
			
		return ret