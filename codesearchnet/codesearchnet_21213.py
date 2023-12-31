def deprecatedMessage(msg, key=None, printStack=False):
	'''
		deprecatedMessage - Print a deprecated messsage (unless they are toggled off). Will print a message only once (based on "key")

		@param msg <str> - Deprecated message to possibly print
		
		@param key <anything> - A key that is specific to this message. 
			If None is provided (default), one will be generated from the md5 of the message.
		        However, better to save cycles and provide a unique key if at all possible.
			The decorator uses the function itself as the key.

		@param printStack <bool> Default False, if True print a stack trace
	'''
	if __deprecatedMessagesEnabled is False:
		return
	if not _alreadyWarned:
		# First warning, let them know how to disable. 
		sys.stderr.write('== DeprecatedWarning: warnings can be disabled by calling IndexedRedis.toggleDeprecatedMessages(False)\n')
	if key is None:
		from .compat_str import tobytes
		key = md5(tobytes(msg)).hexdigest()

	if key not in _alreadyWarned:
		_alreadyWarned[key] = True
		sys.stderr.write('== DeprecatedWarning: %s\n' %(msg, ))
		if printStack:
			sys.stderr.write('  at:\n')
			curStack = traceback.extract_stack()

			sys.stderr.write('  ' + '\n  '.join(traceback.format_list(curStack[:-2])).replace('\t', '    ') + '\n')