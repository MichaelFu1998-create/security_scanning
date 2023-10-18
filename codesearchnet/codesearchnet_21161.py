def copyModel(mdl):
		'''
			copyModel - Copy this model, and return that copy.

			  The copied model will have all the same data, but will have a fresh instance of the FIELDS array and all members,
			    and the INDEXED_FIELDS array.
			  
			  This is useful for converting, like changing field types or whatever, where you can load from one model and save into the other.

			@return <IndexedRedisModel> - A copy class of this model class with a unique name.
		'''
			     
		copyNum = _modelCopyMap[mdl]
		_modelCopyMap[mdl] += 1
		mdlCopy = type(mdl.__name__ + '_Copy' + str(copyNum), mdl.__bases__, copy.deepcopy(dict(mdl.__dict__)))

		mdlCopy.FIELDS = [field.copy() for field in mdl.FIELDS]
		
		mdlCopy.INDEXED_FIELDS = [str(idxField) for idxField in mdl.INDEXED_FIELDS] # Make sure they didn't do INDEXED_FIELDS = FIELDS or something wacky,
											    #  so do a comprehension of str on these to make sure we only get names

		mdlCopy.validateModel()

		return mdlCopy