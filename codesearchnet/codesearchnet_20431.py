def create_virtualenv(self):
        """
        Creates the virtualenv for the project
        
        """
        if check_command('virtualenv'):
            ve_dir = os.path.join(self._ve_dir, self._project_name)
            if os.path.exists(ve_dir):
                if self._force:
                    logging.warn('Removing existing virtualenv')
                    shutil.rmtree(ve_dir)
                else:
                    logging.warn('Found existing virtualenv; not creating (use --force to overwrite)')
                    return
            logging.info('Creating virtualenv')
            p = subprocess.Popen('virtualenv --no-site-packages {0} > /dev/null'.format(ve_dir), shell=True)
            os.waitpid(p.pid, 0)
            # install modules
            for m in self._modules:
                self.log.info('Installing module {0}'.format(m))
                p = subprocess.Popen('{0} install {1} > /dev/null'.format(os.path.join(self._ve_dir, \
                self._project_name) + os.sep + 'bin' + os.sep + 'pip', m), shell=True)
                os.waitpid(p.pid, 0)