def setDefaultIREncoding(encoding):
	'''
		setDefaultIREncoding - Sets the default encoding used by IndexedRedis.
		  This will be the default encoding used for field data. You can override this on a
		  per-field basis by using an IRField (such as IRUnicodeField or IRRawField)

		@param encoding - An encoding (like utf-8)
	'''
	try:
		b''.decode(encoding)
	except:
		raise ValueError('setDefaultIREncoding was provided an invalid codec. Got (encoding="%s")' %(str(encoding), ))

	global defaultIREncoding
	defaultIREncoding = encoding