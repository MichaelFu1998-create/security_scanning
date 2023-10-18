def _filter(filterObj, **kwargs):
		'''
			Internal for handling filters; the guts of .filter and .filterInline
		'''
		for key, value in kwargs.items():
			if key.endswith('__ne'):
				notFilter = True
				key = key[:-4]
			else:
				notFilter = False
			if key not in filterObj.indexedFields:
				raise ValueError('Field "' + key + '" is not in INDEXED_FIELDS array. Filtering is only supported on indexed fields.')

			if notFilter is False:
				filterObj.filters.append( (key, value) )
			else:
				filterObj.notFilters.append( (key, value) )

		return filterObj