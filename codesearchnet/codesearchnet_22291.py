def load_resource(path, root=''):
        """
        .. warning::

            Experiment feature.

            BE CAREFUL! WE MAY REMOVE THIS FEATURE!


        load resource file which in package.
        this method is used to load file easier in different environment.

        e.g:

        consume we have a file named `resource.io` in package `cliez.conf`,
        and we want to load it.
        the easiest way may like this:

        .. code-block:: python

            open('../conf/resource.io').read()


        An obvious problem is `..` is relative path.
        it will cause an error.

        `load_resource` is designed for solve this problem.


        The following code are equivalent:

        .. code-block:: python

            a = Component()
            a.load_resource('resource.io', root='cliez/base')
            a.load_resource('base/resource.io', root='cliez')
            a.load_resource('/base/resource.io', root='cliez')
            a.load_resource('cliez/base/resource.io')
            a.load_resource(__file__.rsplit('/', 2)[0] +
            '/cliez/base/resource.io')


        .. note::

            The document charset *MUST BE* utf-8


        :param str path: file path
        :param str root: root path

        :return: str
        """

        if root:
            full_path = root + '/' + path.strip('/')
        else:
            full_path = path

        buf = ''

        try:
            buf = open(full_path).read()
        except IOError:
            pkg, path = full_path.split('/', 1)
            try:
                import pkg_resources
                buf = pkg_resources.resource_string(pkg, path)
                # compatible python3 and only support utf-8
                if type(buf) != str:
                    buf = buf.decode('utf-8')
                    pass
            except AttributeError:
                # load resource feature not work in python2
                pass

        return buf