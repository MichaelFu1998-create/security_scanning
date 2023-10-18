def create_project(self):
        '''
        Creates a base Django project
        '''
        if os.path.exists(self._py):
            prj_dir = os.path.join(self._app_dir, self._project_name)
            if os.path.exists(prj_dir):
                if self._force:
                    logging.warn('Removing existing project')
                    shutil.rmtree(prj_dir)
                else:
                    logging.warn('Found existing project; not creating (use --force to overwrite)')
                    return
            logging.info('Creating project')
            p = subprocess.Popen('cd {0} ; {1} startproject {2} > /dev/null'.format(self._app_dir, self._ve_dir + os.sep + self._project_name + \
            os.sep + 'bin' + os.sep + 'django-admin.py', self._project_name), \
            shell=True)
            os.waitpid(p.pid, 0)
        else:
            logging.error('Unable to find Python interpreter in virtualenv')
            return