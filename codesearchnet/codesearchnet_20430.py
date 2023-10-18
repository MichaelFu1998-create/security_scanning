def check_directories(self):
        """
        Creates base directories for app, virtualenv, and nginx

        """
        self.log.debug('Checking directories')
        if not os.path.exists(self._ve_dir):
            os.makedirs(self._ve_dir)
        if not os.path.exists(self._app_dir):
            os.makedirs(self._app_dir)
        if not os.path.exists(self._conf_dir):
            os.makedirs(self._conf_dir)
        if not os.path.exists(self._var_dir):
            os.makedirs(self._var_dir)
        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)
        if not os.path.exists(self._script_dir):
            os.makedirs(self._script_dir)

        # copy uswgi_params for nginx
        uwsgi_params = '/etc/nginx/uwsgi_params'
        if os.path.exists(uwsgi_params):
            shutil.copy(uwsgi_params, self._conf_dir)
        else:
            logging.warning('Unable to find Nginx uwsgi_params.  You must manually copy this to {0}.'.format(self._conf_dir))

        # copy mime.types for nginx
        mime_types = '/etc/nginx/mime.types'
        if os.path.exists(mime_types):
            shutil.copy(mime_types, self._conf_dir)
            self._include_mimetypes = True
        else:
            logging.warn('Unable to find mime.types for Nginx.  You must manually copy this to {0}.'.format(self._conf_dir))