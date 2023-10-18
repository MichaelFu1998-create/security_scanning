def install_required(self, type=None, service=None, list_only=0, **kwargs): # pylint: disable=redefined-builtin
        """
        Installs system packages listed as required by services this host uses.
        """
        r = self.local_renderer
        list_only = int(list_only)
        type = (type or '').lower().strip()
        assert not type or type in PACKAGE_TYPES, 'Unknown package type: %s' % (type,)
        lst = []
        if type:
            types = [type]
        else:
            types = PACKAGE_TYPES
        for _type in types:
            if _type == SYSTEM:
                content = '\n'.join(self.list_required(type=_type, service=service))
                if list_only:
                    lst.extend(_ for _ in content.split('\n') if _.strip())
                    if self.verbose:
                        print('content:', content)
                    break
                fd, fn = tempfile.mkstemp()
                fout = open(fn, 'w')
                fout.write(content)
                fout.close()
                self.install_custom(fn=fn)
            else:
                raise NotImplementedError
        return lst