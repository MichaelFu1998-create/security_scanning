def create_manage_scripts(self):
        """
        Creates scripts to start and stop the application

        """
        # create start script
        start = '# start script for {0}\n\n'.format(self._project_name)
        # start uwsgi
        start += 'echo \'Starting uWSGI...\'\n'
        start += 'sh {0}.uwsgi\n'.format(os.path.join(self._conf_dir, self._project_name))
        start += 'sleep 1\n'
        # start nginx
        start += 'echo \'Starting Nginx...\'\n'
        start += 'nginx -c {0}_nginx.conf\n'.format(os.path.join(self._conf_dir, self._project_name))
        start += 'sleep 1\n'
        start += 'echo \'{0} started\'\n\n'.format(self._project_name)

        # stop script
        stop = '# stop script for {0}\n\n'.format(self._project_name)
        # stop nginx
        stop += 'if [ -e {0}_nginx.pid ]; then nginx -c {1}_nginx.conf -s stop ; fi\n'.format(os.path.join(self._var_dir, self._project_name), os.path.join(self._conf_dir, self._project_name))
        # stop uwsgi
        stop += 'if [ -e {0}_uwsgi.pid ]; then kill -9 `cat {0}_uwsgi.pid` ; rm {0}_uwsgi.pid 2>&1 > /dev/null ; fi\n'.format(os.path.join(self._var_dir, self._project_name))
        stop += 'echo \'{0} stopped\'\n'.format(self._project_name)

        # write scripts
        start_file = '{0}_start.sh'.format(os.path.join(self._script_dir, self._project_name))
        stop_file = '{0}_stop.sh'.format(os.path.join(self._script_dir, self._project_name))
        f = open(start_file, 'w')
        f.write(start)
        f.close()
        f = open(stop_file, 'w')
        f.write(stop)
        f.close()
        # make executable
        os.chmod(start_file, 0754)
        os.chmod(stop_file, 0754)