def login(self, oauth_filename="oauth", uploader_id=None):
		"""Authenticate the gmusicapi Musicmanager instance.

		Parameters:
			oauth_filename (str): The filename of the oauth credentials file to use/create for login.
				Default: ``oauth``

			uploader_id (str): A unique id as a MAC address (e.g. ``'00:11:22:33:AA:BB'``).
				This should only be provided in cases where the default (host MAC address incremented by 1) won't work.

		Returns:
			``True`` on successful login, ``False`` on unsuccessful login.
		"""

		cls_name = type(self).__name__

		oauth_cred = os.path.join(os.path.dirname(OAUTH_FILEPATH), oauth_filename + '.cred')

		try:
			if not self.api.login(oauth_credentials=oauth_cred, uploader_id=uploader_id):
				try:
					self.api.perform_oauth(storage_filepath=oauth_cred)
				except OSError:
					logger.exception("\nUnable to login with specified oauth code.")

				self.api.login(oauth_credentials=oauth_cred, uploader_id=uploader_id)
		except (OSError, ValueError):
			logger.exception("{} authentication failed.".format(cls_name))

			return False

		if not self.is_authenticated:
			logger.warning("{} authentication failed.".format(cls_name))

			return False

		logger.info("{} authentication succeeded.\n".format(cls_name))

		return True