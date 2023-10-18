def run(*args):
	"""
	Check and/or create Django migrations.

	If --check is present in the arguments then migrations are checked only.
	"""
	if not settings.configured:
		settings.configure(**DEFAULT_SETTINGS)

	django.setup()

	parent = os.path.dirname(os.path.abspath(__file__))
	sys.path.insert(0, parent)

	if "--check" in args:
		check_migrations()
	else:
		django.core.management.call_command("makemigrations", APP_NAME, *args)