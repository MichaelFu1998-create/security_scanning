def install_from_upstream(self):
        """
        Installs Vagrant from the most recent package available from their homepage.
        """
        from burlap.system import get_arch, distrib_family
        r = self.local_renderer
        content = urlopen(r.env.download_url).read()
        print(len(content))
        matches = DOWNLOAD_LINK_PATTERN.findall(content)
        print(matches)
        arch = get_arch() # e.g. 'x86_64'
        family = distrib_family()
        if family == DEBIAN:
            ext = '.deb'
            matches = [match for match in matches if match.endswith(ext) and arch in match]
            print('matches:', matches)
            assert matches, "No matches found."
            assert len(matches) == 1, "Too many matches found: %s" % (', '.join(matches))
            r.env.final_download_url = matches[0]
            r.env.local_filename = '/tmp/vagrant%s' % ext
            r.run('wget -O {local_filename} {final_download_url}')
            r.sudo('dpkg -i {local_filename}')
        else:
            raise NotImplementedError('Unsupported family: %s' % family)