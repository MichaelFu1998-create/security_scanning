def save(self, cascadeSave=True):
		'''
			save - Save this object.
			
			Will perform an "insert" if this object had not been saved before,
			  otherwise will update JUST the fields changed on THIS INSTANCE of the model.

			  i.e. If you have two processes fetch the same object and change different fields, they will not overwrite
			  eachother, but only save the ones each process changed.

			If you want to save multiple objects of type MyModel in a single transaction,
			and you have those objects in a list, myObjs, you can do the following:

				MyModel.saver.save(myObjs)

			@param cascadeSave <bool> Default True - If True, any Foreign models linked as attributes that have been altered
			   or created will be saved with this object. If False, only this object (and the reference to an already-saved foreign model) will be saved.

			@see #IndexedRedisSave.save

			@return <list> - Single element list, id of saved object (if successful)
		'''
		saver = IndexedRedisSave(self.__class__)
		return saver.save(self, cascadeSave=cascadeSave)