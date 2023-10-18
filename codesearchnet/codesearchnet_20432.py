def create_nginx_config(self):
        """
        Creates the Nginx configuration for the project

        """
        cfg = '# nginx config for {0}\n'.format(self._project_name)
        if not self._shared_hosting:
            # user
            if self._user:
                cfg += 'user {0};\n'.format(self._user)
            # misc nginx config
            cfg += 'worker_processes 1;\nerror_log {0}-errors.log;\n\
pid {1}_    nginx.pid;\n\n'.format(os.path.join(self._log_dir, \
                self._project_name), os.path.join(self._var_dir, self._project_name))
            cfg += 'events {\n\tworker_connections 32;\n}\n\n'
            # http section
            cfg += 'http {\n'
            if self._include_mimetypes:
                cfg += '\tinclude mime.types;\n'
            cfg += '\tdefault_type application/octet-stream;\n'
            cfg += '\tclient_max_body_size 1G;\n'
            cfg += '\tproxy_max_temp_file_size 0;\n'
            cfg += '\tproxy_buffering off;\n'
            cfg += '\taccess_log {0}-access.log;\n'.format(os.path.join \
                (self._log_dir, self._project_name))
            cfg += '\tsendfile on;\n'
            cfg += '\tkeepalive_timeout 65;\n'
            # server section
        cfg += '\tserver {\n'
        cfg += '\t\tlisten 0.0.0.0:{0};\n'.format(self._port)
        if self._server_name:
            cfg += '\t\tserver_name {0};\n'.format(self._server_name)
        # location section
        cfg += '\t\tlocation / {\n'
        cfg += '\t\t\tuwsgi_pass unix:///{0}.sock;\n'.format(\
            os.path.join(self._var_dir, self._project_name))
        cfg += '\t\t\tinclude uwsgi_params;\n'
        cfg += '\t\t}\n\n'
        # end location
        # error page templates
        cfg += '\t\terror_page 500 502 503 504 /50x.html;\n'
        cfg += '\t\tlocation = /50x.html {\n'
        cfg += '\t\t\troot html;\n'
        # end error page section
        cfg += '\t\t}\n'
        # end server section
        cfg += '\t}\n'
        if not self._shared_hosting:
            # end http section
            cfg += '}\n'

        # create conf
        f = open(self._nginx_config, 'w')
        f.write(cfg)
        f.close()