def toIndex(self, value):
		'''
			toIndex - An optional method which will return the value prepped for index.

			By default, "toStorage" will be called. If you provide "hashIndex=True" on the constructor,
			the field will be md5summed for indexing purposes. This is useful for large strings, etc.
		'''
		if self._isIrNull(value):
			ret = IR_NULL_STR
		else:
			ret = self._toIndex(value)

		if self.isIndexHashed is False:
			return ret

		return md5(tobytes(ret)).hexdigest()