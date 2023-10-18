def get_resource(self, p):
        """
        Get metadata for a given file
        """
        for r in self.package['resources']:
            if r['relativepath'] == p:
                r['localfullpath'] = os.path.join(self.rootdir, p)
                return r

        raise Exception("Invalid path")