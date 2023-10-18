def getCompressMod(self):
		'''
			getCompressMod - Return the module used for compression on this field

			@return <module> - The module for compression
		'''
		if self.compressMode == COMPRESS_MODE_ZLIB:
			return zlib
		if self.compressMode == COMPRESS_MODE_BZ2:
			return bz2
		if self.compressMode == COMPRESS_MODE_LZMA:
			# Since lzma is not provided by python core in python2, search out some common alternatives.
			#  Throw exception if we can find no lzma implementation.
			global _lzmaMod
			if _lzmaMod is not None:
				return _lzmaMod
			try:
				import lzma
				_lzmaMod = lzma
				return _lzmaMod
			except:
				# Python2 does not provide "lzma" module, search for common alternatives
				try:
					from backports import lzma
					_lzmaMod = lzma
					return _lzmaMod
				except:
					pass
				try:
					import lzmaffi as lzma
					_lzmaMod = lzma
					return _lzmaMod
				except:
					pass
				raise ImportError("Requested compress mode is lzma and could not find a module providing lzma support. Tried: 'lzma', 'backports.lzma', 'lzmaffi' and none of these were available. Please install one of these, or to use an unlisted implementation, set IndexedRedis.fields.compressed._lzmaMod to the module (must implement standard python compression interface)")