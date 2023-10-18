def hashDictOneLevel(myDict):
	'''
		A function which can generate a hash of a one-level 
		  dict containing strings (like REDIS_CONNECTION_PARAMS)

		@param myDict <dict> - Dict with string keys and values

		@return <long> - Hash of myDict
	'''
	keys = [str(x) for x in myDict.keys()]
	keys.sort()

	lst = []
	for key in keys:
		lst.append(str(myDict[key]) + '__~~__')

	return '+_[,'.join(lst).__hash__()