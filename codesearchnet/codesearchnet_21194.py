def save(self, obj, usePipeline=True, forceID=False, cascadeSave=True, conn=None):
		'''
			save - Save an object / objects associated with this model. 
			
			You probably want to just do object.save() instead of this, but to save multiple objects at once in a single transaction, 
			   you can use:
				
				MyModel.saver.save(myObjs)

			@param obj <IndexedRedisModel or list<IndexedRedisModel> - The object to save, or a list of objects to save

			@param usePipeline - Use a pipeline for saving. You should always want this, unless you are calling this function from within an existing pipeline.

			@param forceID - if not False, force ID to this. If obj is list, this is also list. Forcing IDs also forces insert. Up to you to ensure ID will not clash.
			@param cascadeSave <bool> Default True - If True, any Foreign models linked as attributes that have been altered
			   or created will be saved with this object. If False, only this object (and the reference to an already-saved foreign model) will be saved.

			@param conn - A connection or None

			@note - if no ID is specified

			@return - List of pks
		'''
		if conn is None:
			conn = self._get_connection()

		# If we are in a pipeline, we need an external connection to fetch any potential IDs for inserts.
		if usePipeline is True:
			idConn = conn
		else:
			idConn = self._get_new_connection()

		if issubclass(obj.__class__, (list, tuple)):
			objs = obj
		else:
			objs = [obj]


		if usePipeline is True:
			pipeline = conn.pipeline()
		else:
			pipeline = conn

		oga = object.__getattribute__

		if cascadeSave is True:

			# TODO: Confirm that this pipeline logic works even when doPipeline is False
			#   (i.e. that cascading works through calls to reset)
#			foreignPipelines = OrderedDict()
			foreignSavers = {}

			for thisObj in objs:
				if not thisObj.foreignFields:
					continue

				foreignFields = thisObj.foreignFields
				for foreignField in foreignFields:

					rawObj = oga(thisObj, str(foreignField))

					if rawObj in (None, irNull) or not rawObj.isFetched():
						continue

					foreignObjects = oga(thisObj, str(foreignField)).getObjs()

					for foreignObject in foreignObjects:
						doSaveForeign = False
						if getattr(foreignObject, '_id', None):
							if foreignObject.hasUnsavedChanges(cascadeObjects=True):
								doSaveForeign = True
						else:
							doSaveForeign = True

						# OLD:
						# Assemble each level of Foreign fields into an ordered pipeline. Based on semi-recursion,
						#   we will save the deepest level first in a pipeline, then the next up, on until we complete any subs

						# NEW:
						#   Assemble all foreign fields into current pipeline and execute all in one block
						if doSaveForeign is True:
							if foreignField not in foreignSavers:
#								foreignPipelines[foreignField] = self._get_new_connection().pipeline()
								foreignSavers[foreignField] = IndexedRedisSave(foreignObject.__class__)

							#foreignSavers[foreignField].save(foreignObject, usePipeline=False, cascadeSave=True, conn=foreignPipelines[foreignField])
							foreignSavers[foreignField].save(foreignObject, usePipeline=False, cascadeSave=True, conn=pipeline)

#			if foreignPipelines:
#				for foreignPipeline in foreignPipelines.values():
#					foreignPipeline.execute()

				

		objsLen = len(objs)

		if forceID is not False:
			# Compat with old poor design.. :(
			if isinstance(forceID, (list, tuple)):
				forceIDs = forceID
			else:
				forceIDs = [forceID]
			isInserts = [] 
			i = 0
			while i < objsLen:
				if forceIDs[i] is not False:
					objs[i]._id = forceIDs[i]
					isInserts.append(True)
				else:
					isInsert = not bool(getattr(obj, '_id', None))
					if isInsert is True:
						objs[i]._id = self._getNextID(idConn)
					isInserts.append(isInsert)
				i += 1
		else:
			isInserts = []
			for obj in objs:
				isInsert = not bool(getattr(obj, '_id', None))
				if isInsert is True:
					obj._id = self._getNextID(idConn)
				isInserts.append(isInsert)
				

		ids = [] # Note ids can be derived with all information above..
		i = 0
		while i < objsLen:
			self._doSave(objs[i], isInserts[i], conn, pipeline)
			ids.append(objs[i]._id)
			i += 1

		if usePipeline is True:
			pipeline.execute()

		return ids