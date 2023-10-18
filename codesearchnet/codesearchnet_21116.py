def reload(self):
		'''
			reload - Reload all objects in this list. 
				Updates in-place. To just fetch all these objects again, use "refetch"

			@return - List (same order as current objects) of either exception (KeyError) if operation failed,
			  or a dict of fields changed -> (old, new)
		'''
		if len(self) == 0:
			return []

		ret = []
		for obj in self:
			res = None
			try:
				res = obj.reload()
			except Exception as e:
				res = e

			ret.append(res)

		return ret