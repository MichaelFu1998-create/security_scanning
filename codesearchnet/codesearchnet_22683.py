def ensure_dir_exists(func):
	"wrap a function that returns a dir, making sure it exists"
	@functools.wraps(func)
	def make_if_not_present():
		dir = func()
		if not os.path.isdir(dir):
			os.makedirs(dir)
		return dir
	return make_if_not_present