def dump(self, out_dir='.'):
        """Dump proto file to given directory.
        
        Keyword arguments:
        out_dir -- dump directory. Default='.'
        """
        uri = out_dir + os.sep + self.name
        with open(uri, 'w') as fh:
            fh.write('\n'.join(self.lines))