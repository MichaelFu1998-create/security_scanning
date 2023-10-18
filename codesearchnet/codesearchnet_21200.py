def deleteMultiple(self, objs):
		'''
			deleteMultiple - Delete multiple objects

			@param objs - List of objects

			@return - Number of objects deleted
		'''
		conn = self._get_connection()
		pipeline = conn.pipeline()

		numDeleted = 0

		for obj in objs:
			numDeleted += self.deleteOne(obj, pipeline)

		pipeline.execute()

		return numDeleted