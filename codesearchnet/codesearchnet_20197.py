def evaluate(self, repo, spec, args):
        """
        Evaluate the files identified for checksum.
        """

        status = []

        # Do we have to any thing at all? 
        if len(spec['files']) == 0: 
            return status 

        with cd(repo.rootdir):
            
            rules = None 
            if 'rules-files' in spec and len(spec['rules-files']) > 0: 
                rulesfiles = spec['rules-files']
                rules = {} 
                for f in rulesfiles: 
                    d = json.loads(open(f).read())
                    rules.update(d)
            elif 'rules' in spec: 
                rules = {
                    'inline': spec['rules'] 
                }
                
            if rules is None or len(rules) == 0:
                print("Regression quality validation has been enabled but no rules file has been specified")
                print("Example: { 'min-r2': 0.25 }. Put this either in file or in dgit.json")
                raise InvalidParameters("Regression quality checking rules missing")

            files = dict([(f, open(f).read()) for f in spec['files']])

            for r in rules:
                if 'min-r2' not in rules[r]:
                    continue
                minr2 = float(rules[r]['min-r2'])
                for f in files:
                    match = re.search(r"R-squared:\s+(\d.\d+)", files[f])
                    if match is None:
                        status.append({
                            'target': f,
                            'validator': self.name,
                            'description': self.description,
                            'rules': r,
                            'status': "ERROR",
                            'message': "Invalid model output"
                            })
                    else:
                        r2 = match.group(1)
                        r2 = float(r2)
                        if r2 > minr2:
                            status.append({
                                'target': f,
                                'validator': self.name,
                                'description': self.description,
                                'rules': r,
                                'status': "OK",
                                'message': "Acceptable R2"
                            })
                        else:
                            status.append({
                                'target': f,
                                'validator': self.name,
                                'description': self.description,
                                'rules': r,
                                'status': "ERROR",
                                'message': "R2 is too low"
                            })

        return status