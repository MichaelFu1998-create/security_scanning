def recursive_glob(root, spec):
	"""
	Like iglob, but recurse directories

	>>> any('path.py' in result for result in recursive_glob('.', '*.py'))
	True

	>>> all(result.startswith('.') for result in recursive_glob('.', '*.py'))
	True

	>>> len(list(recursive_glob('.', '*.foo')))
	0

	"""
	specs = (
		os.path.join(dirpath, dirname, spec)
		for dirpath, dirnames, filenames in os.walk(root)
		for dirname in dirnames
	)

	return itertools.chain.from_iterable(
		glob.iglob(spec)
		for spec in specs
	)