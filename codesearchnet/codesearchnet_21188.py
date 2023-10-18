def _doCascadeFetch(obj):
		'''
			_doCascadeFetch - Takes an object and performs a cascading fetch on all foreign links, and all theirs, and so on.

			@param obj <IndexedRedisModel> - A fetched model
		'''
		obj.validateModel()

		if not obj.foreignFields:
			return

		  # NOTE: Currently this fetches using one transaction per object. Implementation for actual resolution is in
		  #   IndexedRedisModel.__getattribute__ 

		for foreignField in obj.foreignFields:
			subObjsData = object.__getattribute__(obj, foreignField)
			if not subObjsData:
				setattr(obj, str(foreignField), irNull)
				continue
			subObjs = subObjsData.getObjs()
			
			for subObj in subObjs:
				if isIndexedRedisModel(subObj):
					IndexedRedisQuery._doCascadeFetch(subObj)