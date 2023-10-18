def create(self):
        """
        Creates the full project

        """
        # create virtualenv
        self.create_virtualenv()
        # create project
        self.create_project()
        # generate uwsgi script
        self.create_uwsgi_script()
        # generate nginx config
        self.create_nginx_config()
        # generate management scripts
        self.create_manage_scripts()
        logging.info('** Make sure to set proper permissions for the webserver user account on the var and log directories in the project root')