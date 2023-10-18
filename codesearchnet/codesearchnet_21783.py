def site_path(self):
        '''Path to environments site-packages'''

        if platform == 'win':
            return unipath(self.path, 'Lib', 'site-packages')

        py_ver = 'python{0}'.format(sys.version[:3])
        return unipath(self.path, 'lib', py_ver, 'site-packages')