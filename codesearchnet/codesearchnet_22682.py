def encode(name, system='NTFS'):
	"""
	Encode the name for a suitable name in the given filesystem
	>>> encode('Test :1')
	'Test _1'
	"""
	assert system == 'NTFS', 'unsupported filesystem'
	special_characters = r'<>:"/\|?*' + ''.join(map(chr, range(32)))
	pattern = '|'.join(map(re.escape, special_characters))
	pattern = re.compile(pattern)
	return pattern.sub('_', name)