def pprint(self, stream=None):
		'''
			pprint - Pretty-print a dict representation of this object.

			@param stream <file/None> - Either a stream to output, or None to default to sys.stdout
		'''
		pprint.pprint(self.asDict(includeMeta=True, forStorage=False, strKeys=True), stream=stream)