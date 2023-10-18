def _spawn_memcached(sock):
	"""Helper function for tests. Spawns a memcached process attached to sock.
	Returns Popen instance. Terminate with p.terminate().
	Note: sock parameter is not checked, and command is executed as shell.
	Use only if you trust that sock parameter. You've been warned.
	"""
	p = subprocess.Popen('memcached -s ' + sock, shell=True)
	time.sleep(0.2) # memcached needs to initialize
	assert p.poll() is None # make sure it's running
	return p