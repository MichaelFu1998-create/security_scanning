def evaluate(self, repo, spec, args):
        """
        Check the integrity of the datapackage.json
        """

        status = []
        with cd(repo.rootdir):
            files = spec.get('files', ['*'])
            resource_files = repo.find_matching_files(files)
            files = glob2.glob("**/*")
            disk_files = [f for f in files if os.path.isfile(f) and f != "datapackage.json"]

            allfiles = list(set(resource_files + disk_files))
            allfiles.sort()

            for f in allfiles:
                if f in resource_files and f in disk_files:
                    r = repo.get_resource(f)
                    coded_sha256 = r['sha256']
                    computed_sha256 = compute_sha256(f)
                    if computed_sha256 != coded_sha256:
                        status.append({
                            'target': f,
                            'rules': "",
                            'validator': self.name,
                            'description': self.description,
                            'status': 'ERROR',
                            'message': "Mismatch in checksum on disk and in datapackage.json"
                        })
                    else:
                        status.append({
                            'target': f,
                            'rules': "",
                            'validator': self.name,
                            'description': self.description,
                            'status': 'OK',
                            'message': ""
                        })
                elif f in resource_files:
                    status.append({
                        'target': f,
                        'rules': "",
                        'validator': self.name,
                        'description': self.description,
                        'status': 'ERROR',
                        'message': "In datapackage.json but not in repo"
                    })
                else:
                    status.append({
                        'target': f,
                        'rules': "",
                        'validator': self.name,
                        'description': self.description,
                        'status': 'ERROR',
                        'message': "In repo but not in datapackage.json"
                        })


        return status