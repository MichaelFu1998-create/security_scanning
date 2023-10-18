def find_matching_files(self, includes):
        """
        For various actions we need files that match patterns
        """

        if len(includes) == 0: 
            return [] 

        files = [f['relativepath'] for f in self.package['resources']]
        includes = r'|'.join([fnmatch.translate(x) for x in includes])

        # Match both the file name as well the path..
        files = [f for f in files if re.match(includes, os.path.basename(f))] + \
                [f for f in files if re.match(includes, f)]
        files = list(set(files))

        return files